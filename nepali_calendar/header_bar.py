import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from . import date_engine as de


class CalendarHeaderBar:
    """Wraps Adw.HeaderBar — plain Python class, not a GObject subclass."""

    def __init__(self):
        self.widget = Adw.HeaderBar()
        self.widget.set_show_end_title_buttons(True)

        # Callbacks set by the window
        self.on_prev = None
        self.on_next = None
        self.on_today = None
        self.on_mode_changed = None   # (mode: "bs"|"ad")
        self.on_lang_changed = None   # (lang: "np"|"en")

        # Left: prev / next navigation
        self._prev_btn = Gtk.Button.new_from_icon_name("go-previous-symbolic")
        self._prev_btn.set_tooltip_text("Previous")
        self._prev_btn.connect("clicked", self._cb_prev)
        self.widget.pack_start(self._prev_btn)

        self._next_btn = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self._next_btn.set_tooltip_text("Next")
        self._next_btn.connect("clicked", self._cb_next)
        self.widget.pack_start(self._next_btn)

        # Center: dynamic title label
        self._title_label = Gtk.Label()
        self._title_label.add_css_class("heading")
        self.widget.set_title_widget(self._title_label)

        # Right: Today button
        self._today_btn = Gtk.Button(label="Today")
        self._today_btn.add_css_class("flat")
        self._today_btn.connect("clicked", self._cb_today)
        self.widget.pack_end(self._today_btn)

        # Right: EN/NP language toggle
        # Label shows what you'll switch TO (i.e. the other lang)
        self._lang_btn = Gtk.ToggleButton(label="EN")
        self._lang_btn.set_tooltip_text("Switch language (English / Nepali)")
        self._lang_btn.add_css_class("flat")
        self._lang_btn.connect("toggled", self._cb_lang)
        self.widget.pack_end(self._lang_btn)

        # Right: BS/AD calendar mode toggle
        # Label shows what you'll switch TO
        self._mode_btn = Gtk.ToggleButton(label="AD")
        self._mode_btn.set_tooltip_text("Switch between BS and AD primary view")
        self._mode_btn.add_css_class("flat")
        self._mode_btn.connect("toggled", self._cb_mode)
        self.widget.pack_end(self._mode_btn)

    # ── callbacks ──────────────────────────────────────────────────────────

    def _cb_prev(self, _):
        if self.on_prev:
            self.on_prev()

    def _cb_next(self, _):
        if self.on_next:
            self.on_next()

    def _cb_today(self, _):
        if self.on_today:
            self.on_today()

    def _cb_mode(self, btn):
        mode = "ad" if btn.get_active() else "bs"
        # Label shows what you can switch back TO
        btn.set_label("BS" if mode == "ad" else "AD")
        if self.on_mode_changed:
            self.on_mode_changed(mode)

    def _cb_lang(self, btn):
        lang = "en" if btn.get_active() else "np"
        btn.set_label("NP" if lang == "en" else "EN")
        if self.on_lang_changed:
            self.on_lang_changed(lang)

    # ── public API ─────────────────────────────────────────────────────────

    def set_title_text(self, text: str):
        self._title_label.set_text(text)

    def set_month_label(self, bs_year: int, bs_month: int, lang: str = "np", cal_mode: str = "bs"):
        """Convenience wrapper — computes and sets the month/year title."""
        self.set_title_text(de.format_month_year_title(bs_year, bs_month, lang, cal_mode))
