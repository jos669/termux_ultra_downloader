import json
import os

from config.settings import DOWNLOADS_BASE_DIR

USER_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "user_settings.json")


def load_user_settings():
    """Carga la configuración del usuario desde el archivo JSON."""
    if os.path.exists(USER_SETTINGS_FILE):
        with open(USER_SETTINGS_FILE) as f:
            return json.load(f)
    return {}


def save_user_settings(settings):
    """Guarda la configuración del usuario en el archivo JSON."""
    with open(USER_SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def get_default_path():
    """Obtiene la ruta de descarga predeterminada del usuario."""
    settings = load_user_settings()
    return settings.get("default_download_path", DOWNLOADS_BASE_DIR)


def set_default_path(new_path):
    """Establece una nueva ruta de descarga predeterminada."""
    settings = load_user_settings()
    settings["default_download_path"] = new_path
    save_user_settings(settings)
    print(f"Nueva ruta de descarga predeterminada establecida: {new_path}")
