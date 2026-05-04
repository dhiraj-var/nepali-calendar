import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from . import date_engine as de
from .holidays import is_holiday


class MiniMonth(Gtk.Box):
    """Compact single-month widget for the year view."""

    def __init__(self, bs_year: int, bs_month: int, lang: str, cal_mode: str, on_click=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.add_css_class("mini-month")

        today_bs = de.get_today_bs()

        # Month title
        title_text = self._month_title(bs_year, bs_month, lang, cal_mode)
        title = Gtk.Label(label=title_text)
        title.set_halign(Gtk.Align.CENTER)
        title.add_css_class("mini-month-title")
        self.append(title)

        # Weekday header row
        wday_box = Gtk.Box(homogeneous=True)
        for name in de.get_weekday_names(lang):
            short = name[:3] if lang == "np" else name[:2]
            lbl = Gtk.Label(label=short)
            lbl.set_hexpand(True)
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.add_css_class("mini-weekday")
            wday_box.append(lbl)
        self.append(wday_box)

        # Day grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(1)
        grid.set_column_spacing(1)
        self.append(grid)

        days = de.get_days_in_month(bs_year, bs_month)
        first_col = de.get_first_weekday(bs_year, bs_month)

        for cell_i in range(42):
            row = cell_i // 7
            col = cell_i % 7
            day = cell_i - first_col + 1

            if cell_i < first_col or day > days:
                lbl = Gtk.Label(label="")
            else:
                bs_date = de.make_bs_date(bs_year, bs_month, day)
                ad_date = de.bs_to_ad(bs_date)
                is_today = (bs_year == today_bs.year and bs_month == today_bs.month and day == today_bs.day)
                is_sat = col == 6
                holiday = is_holiday(bs_year, bs_month, day)

                if cal_mode == "bs":
                    text = de.format_number(day, lang)
                else:
                    text = str(ad_date.day)

                lbl = Gtk.Label(label=text)
                lbl.set_halign(Gtk.Align.CENTER)
                lbl.set_valign(Gtk.Align.CENTER)
                lbl.add_css_class("mini-day")
                if is_today:
                    lbl.add_css_class("mini-today")
                elif is_sat and not is_today:
                    lbl.add_css_class("mini-saturday")
                elif holiday and not is_today:
                    lbl.add_css_class("mini-saturday")

            grid.attach(lbl, col, row, 1, 1)

        # Click to navigate to this month
        if on_click:
            click = Gtk.GestureClick()
            click.connect("released", lambda g, n, x, y: on_click(bs_year, bs_month))
            self.add_controller(click)
            self.set_cursor_from_name("pointer")

    @staticmethod
    def _month_title(bs_year, bs_month, lang, cal_mode):
        if cal_mode == "bs":
            return de.BS_MONTH_NAMES[bs_month - 1] if lang == "np" else de.BS_MONTH_NAMES_EN[bs_month - 1]
        else:
            mid = de.get_days_in_month(bs_year, bs_month) // 2 + 1
            ad = de.make_bs_date(bs_year, bs_month, mid).to_datetime_date()
            return de.AD_MONTH_SHORT[ad.month - 1]


class YearView(Gtk.ScrolledWindow):
    """12-month overview for a single BS year."""

    _COLS = 3

    def __init__(self):
        super().__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self._lang = "np"
        self._cal_mode = "bs"
        self._bs_year = de.get_today_bs().year

        self.on_month_selected = None  # callback(bs_year, bs_month)

        self._outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._grid = Gtk.Grid()
        self._grid.set_row_spacing(10)
        self._grid.set_column_spacing(10)
        self._grid.set_margin_start(12)
        self._grid.set_margin_end(12)
        self._grid.set_margin_top(12)
        self._grid.set_margin_bottom(12)
        self._grid.set_column_homogeneous(True)
        self._outer.append(self._grid)
        self.set_child(self._outer)

        self._build()

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, v: str):
        self._lang = v
        self._rebuild()

    @property
    def cal_mode(self) -> str:
        return self._cal_mode

    @cal_mode.setter
    def cal_mode(self, v: str):
        self._cal_mode = v
        self._rebuild()

    def set_year(self, bs_year: int):
        self._bs_year = bs_year
        self._rebuild()

    def next_year(self):
        self._bs_year += 1
        self._rebuild()

    def prev_year(self):
        self._bs_year -= 1
        self._rebuild()

    def go_today(self):
        self._bs_year = de.get_today_bs().year
        self._rebuild()

    def _rebuild(self):
        child = self._grid.get_first_child()
        while child:
            nxt = child.get_next_sibling()
            self._grid.remove(child)
            child = nxt
        self._build()

    def _build(self):
        for month in range(1, 13):
            row = (month - 1) // self._COLS
            col = (month - 1) % self._COLS
            mini = MiniMonth(
                self._bs_year, month, self._lang, self._cal_mode,
                on_click=self._on_month_click,
            )
            self._grid.attach(mini, col, row, 1, 1)

    def _on_month_click(self, bs_year: int, bs_month: int):
        if self.on_month_selected:
            self.on_month_selected(bs_year, bs_month)
