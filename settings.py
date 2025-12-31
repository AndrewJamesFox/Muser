import json
import os

SETTINGS_PATH = os.path.expanduser("~/.muser_settings.json")

DEFAULT_SETTINGS = {
    "pdf_export_dir": os.path.join(os.path.expanduser("~"), "Downloads")
}

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_PATH, "r") as f:
            data = json.load(f)
            return {**DEFAULT_SETTINGS, **data}
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass
