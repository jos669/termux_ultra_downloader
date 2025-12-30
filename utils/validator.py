import subprocess
import sys

from .colors import Colors


def check_dependencies():
    """
    Verifica si yt-dlp y ffmpeg están instalados.

    Exits the program if dependencies are missing.
    """
    print(f"{Colors.CYAN}[*] Verificando dependencias...{Colors.RESET}")
    missing = []
    try:
        subprocess.run(
            ["yt-dlp", "--version"], capture_output=True, check=True, text=True
        )
        print(f"{Colors.GREEN}[+] yt-dlp encontrado.{Colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("yt-dlp (instalar con: pip install -r " "requirements.txt)")

    try:
        subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, check=True, text=True
        )
        print(f"{Colors.GREEN}[+] ffmpeg encontrado.{Colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("ffmpeg (instalar con: pkg install ffmpeg)")

    if missing:
        print(
            f"\n{Colors.BOLD}{Colors.RED}ERROR: Dependencias faltantes."
            f"{Colors.RESET}"
        )
        for item in missing:
            print(f"  - {item}")
        print(
            f"\n{Colors.YELLOW}Por favor, instala las dependencias." f"{Colors.RESET}"
        )
        sys.exit(1)


def update_yt_dlp():
    """
    Intenta actualizar yt-dlp usando pip.

    Returns:
        None
    """
    print(f"{Colors.CYAN}[*] Intentando actualizar yt-dlp...{Colors.RESET}")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True
        )
        print(f"{Colors.GREEN}[+] yt-dlp actualizado exitosamente.{Colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"{Colors.RED}ERROR: No se pudo actualizar yt-dlp. {e}{Colors.RESET}")


def is_valid_url(url):
    """
    Una validación muy básica de URL.

    Args:
        url (str): URL a validar

    Returns:
        bool: True si la URL es válida, False en caso contrario
    """
    if not url or not isinstance(url, str):
        return False
    return url.startswith("http://") or url.startswith("https://")
