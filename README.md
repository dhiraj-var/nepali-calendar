# Nepali Calendar

A native GTK4 + libadwaita Linux desktop calendar that displays the **Nepali Bikram Sambat (BS)** calendar as the primary view, with corresponding Gregorian (AD) dates shown in each grid cell.

## Features

- BS-primary calendar grid with AD date in each cell
- BS ↔ AD primary view toggle
- Today's date highlighted with accent color circle
- Public holidays highlighted in red (BS 2080–2086 bundled)
- Weekday headers in Devanagari (आइत सोम मंगल बुध बिही शुक्र शनि)
- Automatic light/dark mode via libadwaita
- Window size and position remembered between sessions
- APT-installable `.deb` package — no Snap, no Flatpak

## Installation (Ubuntu / Debian)

### From .deb package

```bash
sudo dpkg -i nepali-calendar_1.0.0-1_all.deb
sudo apt-get install -f   # fix any missing dependencies
nepali-calendar
```

### Development (run directly)

```bash
# 1. Clone / enter project
cd nepali-calendar

# 2. Create venv with system GTK bindings
python3 -m venv --system-site-packages venv
source venv/bin/activate

# 3. Install nepali-datetime
pip install nepali-datetime

# 4. Run
python3 -m nepali_calendar
```

### System dependencies

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

## Building the .deb

```bash
sudo apt install debhelper fakeroot
bash scripts/build-deb.sh
# Output: dist/nepali-calendar_1.0.0-1_all.deb
```

## Calendar Data Updates

BS calendar data comes from the bundled `nepali-datetime` library and covers dates up to ~BS 2100. To update holiday data or get newer BS year support, a new `.deb` release is published. Users update via:

```bash
sudo apt upgrade nepali-calendar
```

## Technology

| Layer | Choice |
|-------|--------|
| Language | Python 3.8+ |
| GUI | GTK4 via PyGObject |
| Theming | libadwaita (Adw) |
| Calendar Data | `nepali-datetime` (PyPI) |
| Packaging | `.deb` via `dpkg-buildpackage` |
