import datetime
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from . import date_engine as de
from .calendar_view import CalendarView
from .week_view import WeekView
from .year_view import YearView
from .header_bar import CalendarHeaderBar
from . import settings as cfg


class NepaliCalendarWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        prefs = cfg.load_settings()
        self.set_default_size(prefs["width"], prefs["height"])
        self.set_title("Nepali Calendar")

        today_bs = de.get_today_bs()
        self._year = today_bs.year
        self._month = today_bs.month
        self._cal_mode = prefs.get("mode", "bs")
        self._lang = prefs.get("lang", "np")

        # ── Views ────────────────────────────────────────────────────────
        self._month_view = CalendarView()
        self._week_view = WeekView()
        self._year_view = YearView()

        self._apply_mode_lang_to_all()

        # Clicking a mini-month in year view → switch to month view
        self._year_view.on_month_selected = self._on_year_month_selected

        # ── View stack + switcher ────────────────────────────────────────
        self._stack = Adw.ViewStack()
        self._stack.add_titled(self._week_view, "week", "Week")
        self._stack.add_titled(self._month_view, "month", "Month")
        self._stack.add_titled(self._year_view, "year", "Year")
        self._stack.set_visible_child_name("month")
        self._stack.connect("notify::visible-child-name", self._on_view_changed)

        view_switcher = Adw.ViewSwitcher()
        view_switcher.set_stack(self._stack)
        view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        view_switcher.set_halign(Gtk.Align.CENTER)

        switcher_box = Gtk.Box()
        switcher_box.set_halign(Gtk.Align.CENTER)
        switcher_box.set_margin_top(4)
        switcher_box.set_margin_bottom(4)
        switcher_box.append(view_switcher)

        # ── Header bar ───────────────────────────────────────────────────
        self._header = CalendarHeaderBar()
        self._header.on_prev = self._on_prev
        self._header.on_next = self._on_next
        self._header.on_today = self._on_today
        self._header.on_mode_changed = self._on_mode
        self._header.on_lang_changed = self._on_lang

        # ── Layout ───────────────────────────────────────────────────────
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(self._header.widget)
        toolbar_view.add_top_bar(switcher_box)
        toolbar_view.set_content(self._stack)

        self.set_content(toolbar_view)
        self.set_size_request(600, 500)
        self.connect("close-request", self._on_close)

        drag = Gtk.GestureDrag()
        drag.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        drag.connect("drag-end", self._on_drag_end)
        self.add_controller(drag)

        self._update_header_title()

    # ── Property helpers ─────────────────────────────────────────────────

    def _current_view(self) -> str:
        return self._stack.get_visible_child_name() or "month"

    def _apply_mode_lang_to_all(self):
        self._month_view.cal_mode = self._cal_mode
        self._month_view.lang = self._lang
        self._week_view.cal_mode = self._cal_mode
        self._week_view.lang = self._lang
        self._year_view.cal_mode = self._cal_mode
        self._year_view.lang = self._lang

    def _update_header_title(self):
        view = self._current_view()
        if view == "month":
            text = de.format_month_year_title(self._year, self._month, self._lang, self._cal_mode)
        elif view == "week":
            week_start = self._week_view.get_week_start()
            text = de.format_week_title(week_start, self._lang, self._cal_mode)
        else:  # year
            text = de.format_year_title(self._year_view._bs_year, self._lang, self._cal_mode)
        self._header.set_title_text(text)

    # ── Navigation callbacks ─────────────────────────────────────────────

    def _on_prev(self):
        view = self._current_view()
        if view == "month":
            self._year, self._month = de.prev_month(self._year, self._month)
            self._month_view.set_month(self._year, self._month)
        elif view == "week":
            self._week_view.prev_week()
        else:
            self._year_view.prev_year()
        self._update_header_title()

    def _on_next(self):
        view = self._current_view()
        if view == "month":
            self._year, self._month = de.next_month(self._year, self._month)
            self._month_view.set_month(self._year, self._month)
        elif view == "week":
            self._week_view.next_week()
        else:
            self._year_view.next_year()
        self._update_header_title()

    def _on_today(self):
        view = self._current_view()
        today_bs = de.get_today_bs()
        if view == "month":
            self._year, self._month = today_bs.year, today_bs.month
            self._month_view.set_month(self._year, self._month)
        elif view == "week":
            self._week_view.go_today()
        else:
            self._year_view.go_today()
        self._update_header_title()

    def _on_view_changed(self, stack, _param):
        self._update_header_title()

    def _on_mode(self, mode: str):
        self._cal_mode = mode
        self._apply_mode_lang_to_all()
        self._update_header_title()

    def _on_lang(self, lang: str):
        self._lang = lang
        self._apply_mode_lang_to_all()
        self._update_header_title()

    def _on_year_month_selected(self, bs_year: int, bs_month: int):
        self._year = bs_year
        self._month = bs_month
        self._month_view.set_month(bs_year, bs_month)
        self._stack.set_visible_child_name("month")

    def _on_drag_end(self, gesture, offset_x, offset_y):
        if self._current_view() == "year":
            return
        if abs(offset_x) < 60 or abs(offset_y) > abs(offset_x) * 0.8:
            return
        if offset_x < 0:
            self._on_next()
        elif offset_x > 0:
            self._on_prev()

    # ── Persistence ──────────────────────────────────────────────────────

    def _on_close(self, _):
        cfg.save_settings({
            "width": self.get_width(),
            "height": self.get_height(),
            "mode": self._cal_mode,
            "lang": self._lang,
        })
        return False
