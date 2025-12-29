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
    """Función para descargar audio desde YouTube."""

    platform = get_platform_name(url)

    if output_path == "/storage/emulated/0/Download" or output_path == "/data/data/com.termux/files/home/downloads":
        base_output_dir = output_path
    else:
        base_output_dir = os.path.join(output_path, platform, "audio")

    create_directories(base_output_dir)

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
