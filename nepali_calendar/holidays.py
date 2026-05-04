import json
import os
from typing import Optional

_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "holidays.json")
_holidays: dict = {}


def _load():
    global _holidays
    if not _holidays:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _holidays = json.load(f)


def is_holiday(bs_year: int, bs_month: int, bs_day: int) -> Optional[str]:
    _load()
    return (
        _holidays
        .get(str(bs_year), {})
        .get(str(bs_month), {})
        .get(str(bs_day))
    )
