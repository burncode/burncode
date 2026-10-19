# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Load independent locale JSON packs; fallback to English for missing keys."""
import json
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent / "locales"

def locale_names():
    return sorted(p.stem for p in LOCALES_DIR.glob("*.json"))

def load_locale(locale):
    if locale not in locale_names():
        raise ValueError(f"Unknown locale {locale!r}; available: {', '.join(locale_names())}")
    data = json.loads((LOCALES_DIR / f"{locale}.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise ValueError(f"Invalid locale pack: {locale}")
    return data

def tr(cfg, key):
    locale = cfg.get("i18n", {}).get("locale", "en")
    base = load_locale("en")
    if locale != "en":
        base.update(load_locale(locale))
    return base.get(key, key)
