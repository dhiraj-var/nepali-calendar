#!/bin/bash
set -e

cd "$(dirname "$0")/.."
ROOT=$(pwd)
PKG="nepali-calendar"
VERSION=$(python3 -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['version'])")
DEB_NAME="${PKG}_${VERSION}-1_all"
BUILD_DIR="${ROOT}/_build/${DEB_NAME}"

echo "==> Building ${DEB_NAME}.deb"

# ── 1. Vendor nepali-datetime ────────────────────────────────────────────
echo "    Vendoring nepali-datetime..."
rm -rf nepali_calendar/vendor
mkdir -p nepali_calendar/vendor
pip install nepali-datetime --target nepali_calendar/vendor --no-deps -q

# ── 2. Create package tree ───────────────────────────────────────────────
rm -rf "$BUILD_DIR"

SHARE="$BUILD_DIR/usr/share/$PKG"
mkdir -p "$SHARE"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/scalable/apps"
mkdir -p "$BUILD_DIR/DEBIAN"

# App package (excluding __pycache__ and vendor subdir — vendor goes to top-level)
cp -r nepali_calendar "$SHARE/"
rm -rf "$SHARE/nepali_calendar/__pycache__"
# Vendor at top-level so PYTHONPATH only needs /usr/share/nepali-calendar
cp -r nepali_calendar/vendor "$SHARE/"
# Remove vendor copy from inside package (it's at top-level)
rm -rf "$SHARE/nepali_calendar/vendor"

# Launcher
install -m 755 scripts/nepali-calendar.sh "$BUILD_DIR/usr/bin/nepali-calendar"

# Desktop entry + icon
install -m 644 data/nepali.calendar.desktop \
    "$BUILD_DIR/usr/share/applications/"
install -m 644 data/icons/nepali-calendar.svg \
    "$BUILD_DIR/usr/share/icons/hicolor/scalable/apps/"

# ── 3. DEBIAN/control ───────────────────────────────────────────────────
INSTALLED_SIZE=$(du -sk "$BUILD_DIR/usr" | cut -f1)

cat > "$BUILD_DIR/DEBIAN/control" <<EOF
Package: nepali-calendar
Version: ${VERSION}-1
Section: utils
Priority: optional
Architecture: all
Installed-Size: ${INSTALLED_SIZE}
Depends: python3 (>= 3.8), python3-gi, python3-gi-cairo, gir1.2-gtk-4.0, gir1.2-adw-1
Maintainer: Dhiraj Shah <me.dhirajshah@gmail.com>
Homepage: https://github.com/dhiraj-var/nepali-calendar
Description: Nepali Bikram Sambat calendar for Linux desktop
 A native GTK4 + libadwaita desktop calendar displaying the Nepali
 Bikram Sambat (BS) calendar as the primary view with Gregorian (AD)
 secondary dates. Features month, week, and year views, EN/NP language
 toggle, public holiday highlighting, and swipe navigation.
EOF

# ── 4. DEBIAN/postinst — update icon cache ───────────────────────────────
cat > "$BUILD_DIR/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
fi
update-desktop-database /usr/share/applications 2>/dev/null || true
EOF
chmod 755 "$BUILD_DIR/DEBIAN/postinst"

# ── 5. Build .deb ────────────────────────────────────────────────────────
mkdir -p dist
dpkg-deb --build --root-owner-group "$BUILD_DIR" "dist/${DEB_NAME}.deb"

echo ""
echo "==> Done!"
ls -lh "dist/${DEB_NAME}.deb"
echo ""
echo "Install with:"
echo "  sudo dpkg -i dist/${DEB_NAME}.deb"
echo "  sudo apt-get install -f   # fix any missing deps"
