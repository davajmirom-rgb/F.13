# config_manager.py
import json
import os

CONFIG_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "scale": 1.0,
    "font_size": 11,
    "currency_symbol": "₽",
    "currency_code": "RUB",
    "animations_enabled": True
}

def load_settings():
    """Загрузка конфигурации из JSON файла"""
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Дополняем отсутствующие ключи, если файл старой версии
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    """Сохранение конфигурации в JSON файл"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(settings_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
