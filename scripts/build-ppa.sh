#!/bin/bash
# Build and upload a source package to Launchpad PPA.
#
# Usage:
#   bash scripts/build-ppa.sh <launchpad-username> [distro]
#
# Examples:
#   bash scripts/build-ppa.sh dhiraj-var noble
#   bash scripts/build-ppa.sh dhiraj-var jammy
#   bash scripts/build-ppa.sh dhiraj-var          # defaults to noble
#
# Requirements: devscripts dput gnupg
#   sudo apt install devscripts dput

set -e

LP_USER="${1:?Usage: $0 <launchpad-username> [noble|jammy]}"
DISTRO="${2:-noble}"
PPA_NAME="nepali-calendar"

cd "$(dirname "$0")/.."
ROOT=$(pwd)

# ── Version ─────────────────────────────────────────────────────────────
UPSTREAM=$(python3 -c \
  "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
DEB_VERSION="${UPSTREAM}-1ppa1~${DISTRO}1"

echo "==> Building source package ${UPSTREAM}-1ppa1~${DISTRO}1 for ${DISTRO}"

# ── Orig tarball ─────────────────────────────────────────────────────────
ORIG_DIR="$(dirname "$ROOT")"
ORIG_TAR="${ORIG_DIR}/nepali-calendar_${UPSTREAM}.orig.tar.gz"

if [ ! -f "$ORIG_TAR" ]; then
  echo "    Creating orig tarball..."
  git archive --format=tar.gz \
    --prefix="nepali-calendar-${UPSTREAM}/" \
    HEAD > "$ORIG_TAR"
fi

# ── Patch changelog for this distro/version ──────────────────────────────
echo "    Updating debian/changelog for ${DISTRO}..."
ORIG_CHANGELOG=$(cat debian/changelog)
cat > debian/changelog <<EOF
nepali-calendar (${DEB_VERSION}) ${DISTRO}; urgency=low

  * PPA build for Ubuntu ${DISTRO}.

 -- Dhiraj Shah <me.dhirajshah@gmail.com>  $(date -R)

EOF
echo "$ORIG_CHANGELOG" >> debian/changelog

# ── Build source package ─────────────────────────────────────────────────
echo "    Running debuild -S -sa..."
GPG_KEY="C0EE327CB245017BC39CDE08772B6CA2FBED84BE"
debuild -S -sa \
  -k"$GPG_KEY" \
  --no-lintian 2>&1

# Restore original changelog
echo "$ORIG_CHANGELOG" > debian/changelog

# ── Upload ───────────────────────────────────────────────────────────────
CHANGES_FILE="${ORIG_DIR}/nepali-calendar_${DEB_VERSION}_source.changes"

echo ""
echo "==> Uploading to ppa:${LP_USER}/${PPA_NAME} ..."
dput "ppa:${LP_USER}/${PPA_NAME}" "$CHANGES_FILE"

echo ""
echo "==> Done! Check build status at:"
echo "    https://launchpad.net/~${LP_USER}/+archive/ubuntu/${PPA_NAME}/+packages"
