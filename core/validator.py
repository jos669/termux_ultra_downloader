import subprocess
import sys

from utils.colors import Colors


def check_dependencies():
    """Verifica si yt-dlp y ffmpeg están instalados."""
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
            f"\n{Colors.YELLOW}Por favor, instala las dependencias y vuelve "
            f"a ejecutar el script.{Colors.RESET}"
        )
        sys.exit(1)
    print(
        f"{Colors.GREEN}[+] Todas las dependencias están instaladas."
        f"{Colors.RESET}\n"
    )


def is_valid_url(url):
    """Una validación muy básica de URL."""
    if not url or not isinstance(url, str):
        return False
    if "http://" in url or "https://" in url:
        return True
    return False
