import json
import os
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "default_download_path": None,  # Will be set dynamically
    "logs_directory": "logs",
    "max_retries": 3,
    "timeout": 30,
    "ffmpeg_path": None,
    "yt_dlp_path": None
}

CONFIG_FILE = os.path.join(os.path.expanduser("~/.termux_ultra_downloader"), "config.json")


def ensure_config_dir():
    """Ensure the config directory exists."""
    config_dir = os.path.dirname(CONFIG_FILE)
    os.makedirs(config_dir, exist_ok=True)


def load_config():
    """Load configuration from file, creating default if needed."""
    ensure_config_dir()
    
    # Set default download path dynamically
    from .settings import get_default_downloads_path
    DEFAULT_CONFIG["default_download_path"] = get_default_downloads_path()
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # Merge with defaults to ensure all keys exist
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
        except (json.JSONDecodeError, IOError):
            # If config file is corrupted, return defaults
            return DEFAULT_CONFIG.copy()
    else:
        # Create default config file
        save_config(DEFAULT_CONFIG.copy())
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False


def get_config_value(key, default=None):
    """Get a specific configuration value."""
    config = load_config()
    return config.get(key, default)


def set_config_value(key, value):
    """Set a specific configuration value."""
    config = load_config()
    config[key] = value
    return save_config(config)


def get_default_path():
    """Get the default download path from config."""
    return get_config_value("default_download_path")


def set_default_path(path):
    """Set the default download path in config."""
    return set_config_value("default_download_path", path)