import os
import subprocess

from utils.colors import Colors
from utils.logger import log_message
from utils.path_manager import create_directories

from .downloader import run_yt_dlp
from .platforms import get_platform_name


def download_audio(
    url,
    output_path,
    format,
    bitrate,
    is_playlist,
    verbose,
    cookies_file,
    dry_run=False,
):
    """
    Función para descargar audio desde YouTube.

    Args:
        url (str): URL del video de donde extraer el audio
        output_path (str): Ruta de salida para el archivo descargado
        format (str): Formato de audio (mp3, wav, etc.)
        bitrate (str): Calidad de audio (best, 0, 1, etc.)
        is_playlist (bool): Indica si la URL es una playlist
        verbose (bool): Mostrar información detallada
        cookies_file (str): Ruta al archivo de cookies
        dry_run (bool): Modo de prueba sin descargar realmente

    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    platform = get_platform_name(url)

    # Security validation: Check if output_path is safe to prevent directory traversal
    from .downloader import is_safe_path
    if not is_safe_path(os.path.expanduser("~"), output_path):
        print(f"{Colors.RED}ERROR: Ruta de salida insegura: {output_path}{Colors.RESET}")
        print(f"{Colors.YELLOW}La ruta de salida debe estar dentro del directorio de usuario para seguridad.{Colors.RESET}")
        return False

    if output_path == "/storage/emulated/0/Download" or output_path == "/data/data/com.termux/files/home/downloads":
        base_output_dir = output_path
    else:
        base_output_dir = os.path.join(output_path, platform, "audio")

    # Validate and create directories safely
    if not create_directories(base_output_dir):
        print(f"{Colors.RED}ERROR: No se pudieron crear los directorios: {base_output_dir}{Colors.RESET}")
        return False

    # Construcción de argumentos de yt-dlp para audio
    output_template = os.path.join(base_output_dir, "%(title)s.%(ext)s")

    base_args = [
        "-x",  # Extraer audio
        "--audio-format", format,  # Formato de audio (mp3, wav, etc.)
        "--audio-quality", bitrate,  # Calidad de audio (best, 0, 1, etc.)
        "--ignore-errors",
        "--continue",
        "--no-overwrites",
        "-o", output_template,
    ]

    if not is_playlist:
        base_args.append("--no-playlist")
    else:
        print(
            f"{Colors.YELLOW}Descargando playlist de audio. "
            f"Los archivos se guardarán en: {base_output_dir}"
            f"{Colors.RESET}"
        )

    try:
        run_yt_dlp(
            args=base_args,
            url=url,
            platform=platform,
            verbose=verbose,
            cookies_file=cookies_file,
            dry_run=dry_run,
        )
        print(f"{Colors.GREEN}Descarga de audio exitosa.{Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error en la descarga de audio: {e}{Colors.RESET}")
        log_message(f"Error en la descarga de audio: {e}", "ERROR", url, platform)
        return False
    except Exception as e:
        print(f"{Colors.RED}Error inesperado en la descarga de audio: {e}{Colors.RESET}")
        log_message(
            f"Error inesperado en la descarga de audio: {e}",
            "ERROR",
            url,
            platform)
        return False
