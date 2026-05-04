#!/bin/bash
export PYTHONPATH="/usr/share/nepali-calendar:/usr/share/nepali-calendar/vendor:${PYTHONPATH}"
exec python3 -m nepali_calendar "$@"
