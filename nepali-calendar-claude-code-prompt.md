# Project: Nepali Calendar — Linux Desktop App

You are building a **native Linux desktop calendar application** called **Nepali Calendar** (`nepali-calendar`).
This is a greenfield project. Before writing any code, create a `TODO.md` at the project root to track progress.
On every future session, **read `TODO.md` first** and continue from where you left off.

---

## GOAL

Build a polished, production-quality GTK4 + Python desktop calendar app for Ubuntu/Debian Linux that:

- Displays the Nepali Bikram Sambat (BS) calendar as the primary view
- Shows the corresponding Gregorian (AD) date in small font within each grid cell
- Supports switching between BS-primary and AD-primary modes
- Is distributable via APT (`.deb` package) — NOT Snap, NOT Flatpak
- Runs on Ubuntu 20.04+ (old and new systems)
- Supports system light and dark mode automatically

---

## TECHNOLOGY STACK (decided — do not deviate without flagging)

| Layer | Choice | Reason |
|---|---|---|
| Language | Python 3.8+ | Pre-installed on all Ubuntu systems, no runtime install needed |
| GUI Framework | GTK4 via PyGObject (`gi.repository.Gtk`) | Native GNOME look, matches Ubuntu's default calendar aesthetic, supports libadwaita theming |
| Theming | libadwaita (`Adw`) | Automatic light/dark mode, GNOME HIG compliant |
| Calendar Data | `nepali-datetime` Python package (PyPI) | Updated Jan 2026, BS/AD conversion, NPT support, Python datetime-compatible API |
| Packaging | `dpkg` `.deb` with `debian/` control files | APT-installable, no Snap/Flatpak |
| Build Tool | `setuptools` + `pyproject.toml` | Standard Python packaging |
| Data Updates | Bundled lookup table from `nepali-datetime` + periodic pip upgrade path | Data lives in the package; update via new `.deb` release |

---

## DATA SOURCE

Use the `nepali-datetime` Python package:

- GitHub: https://github.com/amitgaru2/nepali-datetime
- PyPI: `pip install nepali-datetime`
- Updated: January 2026 ✅
- Covers BS dates up to ~2100 BS
- API mirrors Python's `datetime` module — `nepali_datetime.date.today()`, `nepali_datetime.date(year, month, day)`, `.to_english_date()`, etc.

**To update calendar data in future:** bump `nepali-datetime` version in `requirements.txt` and rebuild the `.deb`.

---

## FEATURES — MVP

### Calendar View

- Month grid layout inspired by Ubuntu's default GNOME Calendar app
- Each cell shows:
  - **BS date** in large font (primary, when in BS mode)
  - **AD date** in small, muted font in the bottom-right corner of the same cell
- Today's date highlighted with an accent color circle
- Weekday header row: Sunday → Saturday in Nepali: आइत, सोम, मंगल, बुध, बिही, शुक्र, शनि
- Public holidays highlighted in red (use a hardcoded `holidays.json` for BS 2080–2086 initially)

### Navigation

- Previous/Next month arrow buttons
- Month + Year label in header (e.g., "बैशाख २०८२")
- "Today" button to jump back to current month

### Mode Toggle

- Toggle button or switch in the header: **BS ↔ AD**
- In BS mode: large BS date, small AD date in bottom-right corner
- In AD mode: large AD date, small BS date in bottom-right corner

### Light/Dark Mode

- Automatically follow the system's color scheme via `Adw.StyleManager`
- No manual toggle needed — it just works

### Window

- Minimum size: 600×500
- Resizable
- Remembers window size and position between sessions (store in `~/.config/nepali-calendar/settings.json`)

---

## FEATURES — Phase 2 (mark in TODO, implement later)

- Event/reminder system (store events in SQLite at `~/.local/share/nepali-calendar/events.db`)
- Nepali public holidays auto-fetched from an upstream JSON (with fallback to bundled data)
- Tithi display (lunar day) per cell
- Year view
- GNOME Shell / panel indicator showing today's BS date in the system tray

---

## PROJECT STRUCTURE

```
nepali-calendar/
├── TODO.md                          ← Track all progress here; read on every session
├── README.md
├── CHANGELOG.md                     ← Track data and app version changes
├── pyproject.toml
├── requirements.txt
├── nepali_calendar/
│   ├── __init__.py
│   ├── main.py                      ← App entry point
│   ├── app.py                       ← Adw.Application subclass
│   ├── window.py                    ← Main window (Adw.ApplicationWindow)
│   ├── calendar_view.py             ← Calendar grid widget (GTK4 Grid)
│   ├── header_bar.py                ← Navigation arrows + month label + mode toggle
│   ├── date_engine.py               ← BS/AD conversion logic using nepali-datetime
│   ├── holidays.py                  ← Bundled holiday data loader
│   ├── settings.py                  ← Persist window state & preferences
│   └── data/
│       ├── holidays.json            ← Nepali public holidays BS 2080–2086
│       └── style.css                ← Custom GTK CSS (today circle, weekend color, muted AD)
├── debian/                          ← .deb packaging files
│   ├── control
│   ├── changelog
│   ├── rules
│   ├── compat
│   └── install
├── data/
│   ├── nepali.calendar.desktop      ← .desktop launcher file for app menu
│   └── icons/
│       └── nepali-calendar.svg      ← App icon (simple, Nepal-themed)
└── scripts/
    └── build-deb.sh                 ← Script to build the .deb package
```

---

## CALENDAR GRID CELL DESIGN

Each cell in the month grid must follow this layout:

```
┌─────────────────┐
│  ३१             │   ← Large BS date (Devanagari numerals)
│           Apr 2 │   ← Small AD date, muted/secondary color, bottom-right
└─────────────────┘
```

- **Today's cell**: accent color circle drawn behind the BS date number
- **Saturday column**: weekend color tint on text (red or orange)
- **Holidays**: text in red
- **Days outside current month** (trailing/leading): shown in muted grey, visually de-emphasized

---

## UBUNTU / GNOME STYLE REFERENCE

Match the aesthetic of `gnome-calendar`:

- Clean card surface (white in light mode, dark in dark mode) for the grid
- Rounded window corners via libadwaita
- Subtle separator between header bar and calendar grid
- Month navigation as `Gtk.Button` with arrow icons (`go-previous-symbolic`, `go-next-symbolic`)
- Use `Adw.HeaderBar` for the title bar
- Use `Adw.ApplicationWindow` as the root window
- Use `Adw.StyleManager.get_default()` to detect and react to color scheme changes

---

## APT PACKAGING REQUIREMENTS

- **Package name**: `nepali-calendar`
- Binary/launcher: `/usr/bin/nepali-calendar`
- App files: `/usr/share/nepali-calendar/`
- `.desktop` file: `/usr/share/applications/nepali.calendar.desktop`
- Icon: `/usr/share/icons/hicolor/scalable/apps/nepali-calendar.svg`
- **Debian `Depends:`**: `python3, python3-gi, python3-gi-cairo, gir1.2-gtk-4.0, gir1.2-adw-1`
- `nepali-datetime` PyPI package: install via `postinst` script using pip, OR vendor it inside the package under `/usr/share/nepali-calendar/vendor/`
- **Target Ubuntu versions**: 20.04 (Focal), 22.04 (Jammy), 24.04 (Noble)
- Build command: `bash scripts/build-deb.sh` which runs `fakeroot debian/rules binary` or `dpkg-buildpackage -us -uc`
- Output `.deb` goes into `dist/`

---

## BUILD & TEST ON THIS MACHINE

This machine is running **Ubuntu 24.04**. After writing all code, do the following to test:

**Step 1 — Install system dependencies:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 libadwaita-1-dev
pip install nepali-datetime --break-system-packages
```

**Step 2 — Run the app directly (dev mode):**
```bash
python3 -m nepali_calendar
```

Confirm the app launches, renders the calendar grid correctly, today is highlighted, BS/AD toggle works, and dark mode follows the system.

**Step 3 — Build the `.deb`:**
```bash
bash scripts/build-deb.sh
```

**Step 4 — Install and verify:**
```bash
sudo dpkg -i dist/nepali-calendar_*.deb
nepali-calendar
```

Fix any runtime errors before marking MVP complete.

---

## TODO.md — CREATE THIS FILE FIRST

Create `TODO.md` at project root with this exact content:

```markdown
# Nepali Calendar — TODO

## Current Status: NOT STARTED

---

## Phase 1 — MVP

- [ ] Project scaffold (pyproject.toml, requirements.txt, folder structure)
- [ ] `date_engine.py` — BS/AD conversion using nepali-datetime library
- [ ] `holidays.json` — compile initial holiday data for BS 2080–2086
- [ ] `calendar_view.py` — month grid widget with dual-date cells
- [ ] `header_bar.py` — navigation arrows, month/year label, BS↔AD toggle
- [ ] `window.py` — main Adw.ApplicationWindow
- [ ] `app.py` + `main.py` — entry point and Adw.Application subclass
- [ ] Light/dark mode via Adw.StyleManager
- [ ] `style.css` — today highlight circle, weekend color, muted AD date style
- [ ] `settings.py` — persist window size/position to ~/.config/nepali-calendar/settings.json
- [ ] Run and test on Ubuntu 24.04 (dev mode)
- [ ] `debian/` packaging files (control, changelog, rules, compat, install)
- [ ] `scripts/build-deb.sh` — build automation
- [ ] `.desktop` launcher file and SVG icon
- [ ] Build `.deb`, install it, confirm it launches from app menu
- [ ] `README.md` — installation and usage instructions
- [ ] `CHANGELOG.md` — initial entry

## Phase 2 — Later

- [ ] SQLite events/reminders system
- [ ] Tithi (lunar day) display per cell
- [ ] Year view
- [ ] GNOME Shell indicator showing today's BS date
- [ ] Auto-fetch updated holiday data from upstream JSON URL
- [ ] Keyboard navigation (arrow keys to move between days)
- [ ] Date converter dialog (standalone popup)
```

---

## IMPORTANT CONSTRAINTS — READ CAREFULLY

1. **No Snap. No Flatpak. APT `.deb` only.**
2. **No Tkinter. No Qt.** GTK4 + libadwaita exclusively for the native GNOME look.
3. **Devanagari support**: All month names and weekday labels must be in Nepali Unicode (Devanagari script). Use Python Unicode strings directly — no external font dependencies needed.
4. **BS month lengths are NOT computable** — they vary per year and come from a lookup table inside `nepali-datetime`. Never hardcode month lengths manually; always use the library API.
5. **GTK version fallback**: GTK4 + libadwaita requires Ubuntu 22.04+. For Ubuntu 20.04 compatibility, detect the available GTK version at runtime and fall back to GTK3 (`gi.require_version('Gtk', '3.0')`) with a compatibility layer in `app.py`. Document this clearly.
6. **Window state persistence**: Always save and restore last window size and position via `~/.config/nepali-calendar/settings.json`.
7. **Holiday data sourcing**: Compile initial holiday data manually or reference https://github.com/sauzanniraula/Todo_Nepali_Patro for BS 2082 data. Cross-check with official Nepal government calendar. Store as a bundled `holidays.json`.
8. **Future data updates**: Document in `README.md` and `CHANGELOG.md` that BS calendar data updates ship as new `.deb` releases. Users run `sudo apt upgrade nepali-calendar` to get updated data.
9. **Session continuity**: At the start of every new Claude Code session, read `TODO.md` before doing anything else. Update checkboxes as tasks are completed.
