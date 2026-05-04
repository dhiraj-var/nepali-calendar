import json
import os

_CONFIG_DIR = os.path.expanduser("~/.config/nepali-calendar")
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "settings.json")

_DEFAULTS = {"width": 760, "height": 600, "mode": "bs", "lang": "np"}


def load_settings() -> dict:
    try:
        with open(_CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {**_DEFAULTS, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULTS)


def save_settings(settings: dict) -> None:
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
