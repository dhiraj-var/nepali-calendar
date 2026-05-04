#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "==> Vendoring nepali-datetime..."
rm -rf nepali_calendar/vendor
mkdir -p nepali_calendar/vendor
pip install nepali-datetime --target nepali_calendar/vendor --no-deps -q

echo "==> Building .deb package..."
dpkg-buildpackage -us -uc -b --no-sign

echo "==> Moving .deb to dist/..."
mkdir -p dist
mv ../nepali-calendar_*.deb dist/ 2>/dev/null || \
  find .. -maxdepth 1 -name 'nepali-calendar_*.deb' -exec mv {} dist/ \;

echo "==> Done! Package:"
ls -lh dist/nepali-calendar_*.deb
