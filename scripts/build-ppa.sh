#!/bin/bash
# Build and upload a source package to Launchpad PPA.
#
# Usage:
#   bash scripts/build-ppa.sh <launchpad-username> [distro]
#
# Examples:
#   bash scripts/build-ppa.sh dhiraj-var noble
#   bash scripts/build-ppa.sh dhiraj-var jammy
#
# Requirements: devscripts dput gnupg pip
#   sudo apt install devscripts dput

set -e

LP_USER="${1:?Usage: $0 <launchpad-username> [noble|jammy]}"
DISTRO="${2:-noble}"
PPA_NAME="nep-cal"
GPG_KEY="C0EE327CB245017BC39CDE08772B6CA2FBED84BE"

cd "$(dirname "$0")/.."
ROOT=$(pwd)

UPSTREAM=$(python3 -c \
  "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
DEB_VERSION="${UPSTREAM}-1ppa1~${DISTRO}1"
PKG="nepali-calendar"

echo "==> Building ${PKG} ${DEB_VERSION} for ${DISTRO}"

# ── Clean temp working directory ─────────────────────────────────────────
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
SRC_DIR="${WORK}/${PKG}-${UPSTREAM}"

# ── Export clean source from git ─────────────────────────────────────────
echo "    Exporting clean source from git..."
git archive --format=tar.gz --prefix="${PKG}-${UPSTREAM}/" HEAD \
  | tar -C "$WORK" -xzf -

# ── Vendor nepali-datetime into the source ───────────────────────────────
# This goes into the orig tarball so Launchpad's build machine has it.
echo "    Vendoring nepali-datetime into source..."
pip install nepali-datetime \
  --target "${SRC_DIR}/nepali_calendar/vendor" \
  --no-deps -q
# Remove __pycache__ to keep the orig tarball clean
find "${SRC_DIR}/nepali_calendar/vendor" -name '__pycache__' -type d \
  -exec rm -rf {} + 2>/dev/null || true
find "${SRC_DIR}/nepali_calendar/vendor" -name '*.pyc' -delete 2>/dev/null || true

# ── Create orig tarball (includes vendored nepali-datetime) ──────────────
echo "    Creating orig tarball..."
tar -C "$WORK" -czf "${WORK}/${PKG}_${UPSTREAM}.orig.tar.gz" "${PKG}-${UPSTREAM}"

# ── Inject PPA changelog entry ───────────────────────────────────────────
echo "    Setting changelog to ${DEB_VERSION}..."
{
  printf '%s (%s) %s; urgency=low\n\n' "$PKG" "$DEB_VERSION" "$DISTRO"
  printf '  * PPA build for Ubuntu %s.\n\n' "$DISTRO"
  printf ' -- Dhiraj Shah <me.dhirajshah@gmail.com>  %s\n\n' "$(date -R)"
  cat "${SRC_DIR}/debian/changelog"
} > "${SRC_DIR}/debian/changelog.new"
mv "${SRC_DIR}/debian/changelog.new" "${SRC_DIR}/debian/changelog"

# ── Build source package ──────────────────────────────────────────────────
# -S  source only, -sa include orig tarball, -d skip build-dep check,
# -nc skip rules clean (dh not installed locally; Launchpad has it)
echo "    Building source package..."
cd "$SRC_DIR"
dpkg-buildpackage -S -sa -d -nc --no-sign 2>&1

# ── Sign .dsc and .changes ───────────────────────────────────────────────
cd "$WORK"
echo "    Signing..."
debsign -k"$GPG_KEY" "${PKG}_${DEB_VERSION}_source.changes"

# ── Upload ───────────────────────────────────────────────────────────────
echo ""
echo "==> Uploading to ppa:${LP_USER}/${PPA_NAME} ..."
dput "ppa:${LP_USER}/${PPA_NAME}" "${WORK}/${PKG}_${DEB_VERSION}_source.changes"

echo ""
echo "==> Done! Build status:"
echo "    https://launchpad.net/~${LP_USER}/+archive/ubuntu/${PPA_NAME}/+packages"
