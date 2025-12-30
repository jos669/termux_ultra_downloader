import json
import os

from .config_manager import get_default_path as get_config_default_path, set_default_path as set_config_default_path

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
    # Use the new config manager instead of the old settings
    return get_config_default_path()


def set_default_path(new_path):
    """Establece una nueva ruta de descarga predeterminada."""
    # Use the new config manager instead of the old settings
    success = set_config_default_path(new_path)
    if success:
        print(f"Nueva ruta de descarga predeterminada establecida: {new_path}")
    return success
