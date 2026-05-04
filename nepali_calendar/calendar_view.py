import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from . import date_engine as de
from .holidays import is_holiday

_CIRCLE_SIZE = 46  # px — fixed size for today circle


class DayCell(Gtk.Box):
    """Single calendar day cell with a primary date + secondary date."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("day-cell")
        self.set_hexpand(True)
        self.set_vexpand(True)

        # Top section: centered overlay (circle bg + primary label on top)
        top = Gtk.Box()
        top.set_halign(Gtk.Align.CENTER)
        top.set_valign(Gtk.Align.CENTER)
        top.set_vexpand(True)
        self.append(top)

        overlay = Gtk.Overlay()
        overlay.set_halign(Gtk.Align.CENTER)
        overlay.set_valign(Gtk.Align.CENTER)
        top.append(overlay)

        # Circle background — fixed size so border-radius:50% is always circular
        self._circle = Gtk.Box()
        self._circle.set_halign(Gtk.Align.CENTER)
        self._circle.set_valign(Gtk.Align.CENTER)
        self._circle.set_size_request(_CIRCLE_SIZE, _CIRCLE_SIZE)
        overlay.set_child(self._circle)

        # Primary date label — overlaid centered on the circle
        self._primary = Gtk.Label()
        self._primary.set_halign(Gtk.Align.CENTER)
        self._primary.set_valign(Gtk.Align.CENTER)
        self._primary.add_css_class("primary-date")
        overlay.add_overlay(self._primary)

        # Bottom: secondary date (small, right-aligned)
        self._secondary = Gtk.Label()
        self._secondary.set_halign(Gtk.Align.END)
        self._secondary.set_valign(Gtk.Align.END)
        self._secondary.add_css_class("secondary-date")
        self._secondary.set_margin_end(4)
        self._secondary.set_margin_bottom(2)
        self.append(self._secondary)

    def set_day(
        self,
        primary_text: str,
        secondary_text: str,
        is_today: bool,
        is_saturday: bool,
        is_holiday_day: bool,
        outside_month: bool,
    ):
        self._primary.set_text(primary_text)
        self._secondary.set_text(secondary_text)

        for cls in ["today-circle"]:
            self._circle.remove_css_class(cls)
        for cls in ["saturday", "holiday", "today-primary", "outside-month"]:
            self._primary.remove_css_class(cls)
        if outside_month:
            self.add_css_class("outside-month")
        else:
            self.remove_css_class("outside-month")

        if is_today:
            self._circle.add_css_class("today-circle")
            self._primary.add_css_class("today-primary")
        elif is_saturday and not outside_month:
            self._primary.add_css_class("saturday")
        elif is_holiday_day and not outside_month:
            self._primary.add_css_class("holiday")

    def clear(self):
        self._primary.set_text("")
        self._secondary.set_text("")
        self._circle.remove_css_class("today-circle")
        self.remove_css_class("outside-month")


class CalendarView(Gtk.Box):
    """Month grid view."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("calendar-grid")

        self._cal_mode = "bs"
        self._lang = "np"
        today = de.get_today_bs()
        self._year = today.year
        self._month = today.month

        self._weekday_labels: list[Gtk.Label] = []
        self._cells: list[DayCell] = []

        self._build_header()
        self._build_grid()
        self.refresh()

    def _build_header(self):
        self._header_box = Gtk.Box(homogeneous=True)
        names = de.get_weekday_names(self._lang)
        for name in names:
            lbl = Gtk.Label(label=name)
            lbl.set_hexpand(True)
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.add_css_class("weekday-header")
            self._header_box.append(lbl)
            self._weekday_labels.append(lbl)
        self.append(self._header_box)

    def _build_grid(self):
        self._grid = Gtk.Grid()
        self._grid.set_row_homogeneous(True)
        self._grid.set_column_homogeneous(True)
        self._grid.set_hexpand(True)
        self._grid.set_vexpand(True)
        self.append(self._grid)

        for row in range(6):
            for col in range(7):
                cell = DayCell()
                self._grid.attach(cell, col, row, 1, 1)
                self._cells.append(cell)

    def _update_weekday_headers(self):
        for lbl, name in zip(self._weekday_labels, de.get_weekday_names(self._lang)):
            lbl.set_text(name)

    @property
    def cal_mode(self) -> str:
        return self._cal_mode

    @cal_mode.setter
    def cal_mode(self, value: str):
        self._cal_mode = value
        self.refresh()

    # Keep backward-compat alias used by old window.py code
    @property
    def mode(self) -> str:
        return self._cal_mode

    @mode.setter
    def mode(self, value: str):
        self.cal_mode = value

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str):
        self._lang = value
        self._update_weekday_headers()
        self.refresh()

    def set_month(self, bs_year: int, bs_month: int):
        self._year = bs_year
        self._month = bs_month
        self.refresh()

    def refresh(self):
        today_bs = de.get_today_bs()
        days_in_month = de.get_days_in_month(self._year, self._month)
        first_col = de.get_first_weekday(self._year, self._month)

        prev_year, prev_month = de.prev_month(self._year, self._month)
        next_year, next_month = de.next_month(self._year, self._month)
        days_in_prev = de.get_days_in_month(prev_year, prev_month)

        for i, cell in enumerate(self._cells):
            cell_day = i - first_col + 1
            col = i % 7

            if i < first_col:
                prev_day = days_in_prev - (first_col - 1 - i)
                self._fill_outside(cell, prev_year, prev_month, prev_day, col)
            elif cell_day > days_in_month:
                self._fill_outside(cell, next_year, next_month, cell_day - days_in_month, col)
            else:
                bs_date = de.make_bs_date(self._year, self._month, cell_day)
                ad_date = de.bs_to_ad(bs_date)
                is_today = (
                    self._year == today_bs.year
                    and self._month == today_bs.month
                    and cell_day == today_bs.day
                )
                is_sat = col == 6
                holiday = is_holiday(self._year, self._month, cell_day)

                if self._cal_mode == "bs":
                    primary = de.format_number(cell_day, self._lang)
                    secondary = ad_date.strftime("%-d %b")
                else:
                    primary = str(ad_date.day)
                    secondary = de.format_number(cell_day, self._lang)

                cell.set_day(primary, secondary, is_today, is_sat, bool(holiday), False)

    def _fill_outside(self, cell: DayCell, year: int, month: int, day: int, col: int):
        try:
            bs_date = de.make_bs_date(year, month, day)
            ad_date = de.bs_to_ad(bs_date)
            if self._cal_mode == "bs":
                primary = de.format_number(day, self._lang)
                secondary = ad_date.strftime("%-d %b")
            else:
                primary = str(ad_date.day)
                secondary = de.format_number(day, self._lang)
            cell.set_day(primary, secondary, False, col == 6, False, True)
        except Exception:
            cell.clear()
