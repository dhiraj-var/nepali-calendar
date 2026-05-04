import sys
import os
import gi

# When installed as .deb, prepend vendored nepali-datetime path
_vendor = "/usr/share/nepali-calendar/vendor"
if os.path.isdir(_vendor) and _vendor not in sys.path:
    sys.path.insert(0, _vendor)

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Adw, Gdk

from .window import NepaliCalendarWindow

_CSS_FILE = os.path.join(os.path.dirname(__file__), "data", "style.css")


class NepaliCalendarApp(Adw.Application):

    def __init__(self):
        super().__init__(application_id="com.github.nepali.calendar")
        self.connect("activate", self._on_activate)

    def _on_activate(self, _):
        self._load_css()
        win = NepaliCalendarWindow(application=self)
        win.set_size_request(600, 500)
        win.present()

    def _load_css(self):
        provider = Gtk.CssProvider()
        try:
            provider.load_from_path(_CSS_FILE)
        except Exception as e:
            print(f"Warning: could not load CSS: {e}", file=sys.stderr)
        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(
                display,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
