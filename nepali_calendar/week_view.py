import datetime
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from . import date_engine as de
from .holidays import is_holiday

_CIRCLE_SIZE = 52


class WeekCard(Gtk.Box):
    """Self-contained card for a single day in the week view.

    Layout (top → bottom):
      day name label  (small, bold — e.g. "आइतबार" / "Sun")
      [vexpand space]
        date circle overlay  (large number, accent circle for today)
      [vexpand space]
      secondary date  (muted — AD date in BS mode, BS date in AD mode)
    """

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add_css_class("week-card")
        self.set_hexpand(True)
        self.set_vexpand(True)

        # Day name at top
        self._day_name = Gtk.Label()
        self._day_name.set_halign(Gtk.Align.CENTER)
        self._day_name.set_margin_top(10)
        self._day_name.set_margin_bottom(4)
        self._day_name.add_css_class("week-day-name")
        self.append(self._day_name)

        # Centre section: circle + primary date (vertically centred, expands)
        center = Gtk.Box()
        center.set_halign(Gtk.Align.CENTER)
        center.set_valign(Gtk.Align.CENTER)
        center.set_vexpand(True)
        self.append(center)

        overlay = Gtk.Overlay()
        overlay.set_halign(Gtk.Align.CENTER)
        overlay.set_valign(Gtk.Align.CENTER)
        center.append(overlay)

        self._circle = Gtk.Box()
        self._circle.set_halign(Gtk.Align.CENTER)
        self._circle.set_valign(Gtk.Align.CENTER)
        self._circle.set_size_request(_CIRCLE_SIZE, _CIRCLE_SIZE)
        overlay.set_child(self._circle)

        self._primary = Gtk.Label()
        self._primary.set_halign(Gtk.Align.CENTER)
        self._primary.set_valign(Gtk.Align.CENTER)
        self._primary.add_css_class("week-primary-date")
        overlay.add_overlay(self._primary)

        # Secondary date at bottom
        self._secondary = Gtk.Label()
        self._secondary.set_halign(Gtk.Align.CENTER)
        self._secondary.set_valign(Gtk.Align.CENTER)
        self._secondary.add_css_class("secondary-date")
        self._secondary.set_margin_top(6)
        self._secondary.set_margin_bottom(10)
        self.append(self._secondary)

    def set_day(
        self,
        day_name: str,
        primary: str,
        secondary: str,
        is_today: bool,
        is_saturday: bool,
        is_holiday_day: bool,
    ):
        self._day_name.set_text(day_name)
        self._primary.set_text(primary)
        self._secondary.set_text(secondary)

        # Reset all state-dependent classes
        for cls in ["week-card-today", "week-card-saturday"]:
            self.remove_css_class(cls)
        self._circle.remove_css_class("today-circle")
        for cls in ["today-primary", "saturday", "holiday"]:
            self._primary.remove_css_class(cls)
        for cls in ["week-day-name-today", "week-day-name-saturday"]:
            self._day_name.remove_css_class(cls)

        if is_today:
            self.add_css_class("week-card-today")
            self._circle.add_css_class("today-circle")
            self._primary.add_css_class("today-primary")
            self._day_name.add_css_class("week-day-name-today")
        elif is_saturday:
            self.add_css_class("week-card-saturday")
            self._primary.add_css_class("saturday")
            self._day_name.add_css_class("week-day-name-saturday")
        elif is_holiday_day:
            self._primary.add_css_class("holiday")


class WeekView(Gtk.Box):
    """Seven-day week view — 7 WeekCard columns filling the window."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self._cal_mode = "bs"
        self._lang = "np"
        self._ref_ad = datetime.date.today()

        self._cards: list[WeekCard] = []
        self._build()
        self.refresh()

    def _build(self):
        row = Gtk.Box(homogeneous=True)
        row.set_hexpand(True)
        row.set_vexpand(True)
        row.set_margin_start(8)
        row.set_margin_end(8)
        row.set_margin_top(8)
        row.set_margin_bottom(8)
        for _ in range(7):
            card = WeekCard()
            row.append(card)
            self._cards.append(card)
        self.append(row)

    # ── Properties ───────────────────────────────────────────────────────

    @property
    def cal_mode(self) -> str:
        return self._cal_mode

    @cal_mode.setter
    def cal_mode(self, v: str):
        self._cal_mode = v
        self.refresh()

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, v: str):
        self._lang = v
        self.refresh()

    # ── Navigation ───────────────────────────────────────────────────────

    def set_week(self, ref_ad: datetime.date):
        self._ref_ad = ref_ad
        self.refresh()

    def get_week_start(self) -> datetime.date:
        return de.get_week_start_ad(self._ref_ad)

    def next_week(self):
        self._ref_ad += datetime.timedelta(days=7)
        self.refresh()

    def prev_week(self):
        self._ref_ad -= datetime.timedelta(days=7)
        self.refresh()

    def go_today(self):
        self._ref_ad = datetime.date.today()
        self.refresh()

    # ── Data ─────────────────────────────────────────────────────────────

    def refresh(self):
        today_ad = datetime.date.today()
        week_start = de.get_week_start_ad(self._ref_ad)
        day_names = de.get_weekday_names(self._lang)

        for col, card in enumerate(self._cards):
            ad = week_start + datetime.timedelta(days=col)
            bs = de.ad_to_bs(ad)
            is_today = ad == today_ad
            is_sat = col == 6
            holiday = is_holiday(bs.year, bs.month, bs.day)

            if self._cal_mode == "bs":
                primary = de.format_number(bs.day, self._lang)
                secondary = ad.strftime("%-d %b %Y")
            else:
                primary = str(ad.day)
                secondary = (
                    de.BS_MONTH_NAMES_EN[bs.month - 1] + " "
                    + de.format_number(bs.day, self._lang)
                )

            card.set_day(day_names[col], primary, secondary, is_today, is_sat, bool(holiday))
