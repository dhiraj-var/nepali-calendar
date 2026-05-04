# Nepali Calendar — TODO

## Current Status: v1.1.1 COMPLETE (dev mode)

---

## Phase 1 — MVP ✅

- [x] Project scaffold (pyproject.toml, requirements.txt, folder structure)
- [x] venv with --system-site-packages + nepali-datetime installed
- [x] `date_engine.py` — BS/AD conversion using nepali-datetime library
- [x] `holidays.json` — compile initial holiday data for BS 2080–2086
- [x] `holidays.py` — holiday data loader
- [x] `style.css` — today highlight circle, weekend color, muted AD date style
- [x] `settings.py` — persist window size/position/mode/lang
- [x] `calendar_view.py` — month grid widget with dual-date cells
- [x] `week_view.py` — 7-day week view with swipe navigation
- [x] `year_view.py` — 12-month overview with clickable mini-months
- [x] `header_bar.py` — navigation arrows, month/year label, BS↔AD, EN↔NP toggles
- [x] `window.py` — Adw.ViewStack (Week/Month/Year), full state management
- [x] Light/dark mode via Adw.StyleManager (automatic)
- [x] Run and test on Ubuntu 24.04 (dev mode) ✅
- [x] `debian/` packaging files (control, changelog, rules, compat)
- [x] `scripts/build-deb.sh` — build automation
- [x] `.desktop` launcher file and SVG icon
- [ ] Build `.deb`, install it, confirm it launches from app menu
- [x] `README.md` + `CHANGELOG.md`

## v1.1.0 fixes & features ✅

- [x] BS/AD toggle button label updates correctly (shows "BS" when in AD mode, "AD" when in BS mode)
- [x] Today circle properly centered using Gtk.Overlay (46×46 fixed circle bg)
- [x] Font sizes increased (primary 1.45em, secondary 0.82em)
- [x] EN/NP language switch — all labels, month names, day numbers
- [x] Full Nepali weekday names (आइतबार, सोमबार, मंगलबार, बुधबार, बिहिबार, शुक्रबार, शनिबार)
- [x] Swipe left/right gesture to navigate months/weeks
- [x] Week view, Month view, Year view with Adw.ViewSwitcher
- [x] AD mode month label correctly shows AD month/year (e.g., "April 2026")

## Phase 2 — Later

- [ ] SQLite events/reminders system
- [ ] Tithi (lunar day) display per cell
- [ ] GNOME Shell indicator showing today's BS date
- [ ] Auto-fetch updated holiday data from upstream JSON URL
- [ ] Keyboard navigation (arrow keys to move between days)
- [ ] Date converter dialog (standalone popup)
- [ ] Tablet/touch optimization
