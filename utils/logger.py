# (Sin cambios)
import os
from datetime import datetime

from config.settings import get_log_file, get_logs_dir

from .colors import Colors


def log_message(message, level="INFO", url=None, platform=None):
    """Escribe un mensaje en el archivo de log."""
    try:
        log_file = get_log_file()
        logs_dir = get_logs_dir()
        os.makedirs(logs_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        if platform:
            log_entry += f" [Platform: {platform}]"
        if url:
            log_entry += f" [URL: {url}]"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    except Exception as e:
        print(f"{Colors.RED}Error al escribir en el log: {e}{Colors.RESET}")
