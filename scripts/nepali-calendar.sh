#!/bin/bash
# Launcher script for installed .deb package
export PYTHONPATH="/usr/share/nepali-calendar/vendor:${PYTHONPATH}"
exec python3 -m nepali_calendar "$@"
