# Changelog

## [1.1.2] - 2026-05-04

### Fixed
- Swipe gesture now works reliably: moved `GestureDrag` from individual view widgets to the top-level `NepaliCalendarWindow` with `CAPTURE` propagation phase. This ensures pointer events are intercepted before `Adw.ViewStack` page isolation can swallow them. Year view is excluded from swipe navigation.

## [1.1.1] - 2026-05-04

### Fixed
- Swipe gesture now works: switched to `CAPTURE` propagation phase so the gesture fires before child widgets (DayCell overlays, labels) absorb the pointer events. Threshold also lowered from 300 → 150 px/s.

### Changed
- **Week view completely redesigned**: each day is now a self-contained card with the weekday name inside the card at the top, a large centred date number (with today circle), and the secondary date at the bottom. Today's card gets an accent-tinted background and border. Saturday's card has red text for both the day name and date number.

## [1.1.0] - 2026-05-04

### Fixed
- BS/AD toggle button label now updates correctly: shows "BS" when viewing AD, "AD" when viewing BS
- Today's date circle is now perfectly centered using `Gtk.Overlay` with a fixed 46×46 background box
- AD calendar mode now shows the correct AD month/year in the header (e.g., "April 2026" not "बैशाख २०८३")

### Changed
- Font sizes increased: primary date 1.45em, secondary date 0.82em (more readable at all window sizes)
- Nepali weekday headers now show full names: आइतबार, सोमबार, मंगलबार, बुधबार, बिहिबार, शुक्रबार, शनिबार
- Default window size increased to 760×600

### Added
- **EN/NP language toggle** — switch all labels, month names, day numbers between Nepali/Devanagari and English
- **Swipe gesture** — swipe left/right on the calendar to navigate months/weeks (300 px/s threshold)
- **Week view** — single-week view with tall day cells; swipe and arrow navigation in 7-day steps
- **Year view** — 12 mini-month overview for the whole BS year; click any month to jump to it
- **View switcher bar** (Week / Month / Year) using `Adw.ViewSwitcher` + `Adw.ViewStack`
- Language preference (`lang`) persisted in `~/.config/nepali-calendar/settings.json`

## [1.0.0] - 2026-05-04

### Added
- Initial MVP release
- GTK4 + libadwaita native desktop calendar
- Nepali Bikram Sambat (BS) primary calendar view
- Gregorian (AD) secondary dates in each grid cell
- BS ↔ AD mode toggle in the header bar
- Today's date accent highlight (system accent color circle)
- Public holidays for BS 2080–2086 (bundled `holidays.json`)
- Saturday column and holiday text in red
- Days outside current month shown dimmed
- Weekday headers in Devanagari script
- Month/year label in Devanagari numerals and script
- Prev/Next month navigation with arrow buttons
- "Today" button to jump to current month
- Automatic light/dark mode via `Adw.StyleManager`
- Window size and mode persisted in `~/.config/nepali-calendar/settings.json`
- `nepali-datetime` 1.0.8 bundled as vendor dependency in `.deb`
- APT-installable `.deb` package targeting Ubuntu 22.04 / 24.04

### Data
- `nepali-datetime` version: 1.0.8 (January 2026 release, covers BS dates to ~2100)
- Holiday data: BS 2080–2086 (manually compiled; cross-referenced with official Nepal calendar)

### Notes
- Ubuntu 20.04 (Focal): GTK4 + libadwaita not available in default repos; requires Ubuntu 22.04+
- To update BS calendar data: bump `nepali-datetime` version and rebuild `.deb`
