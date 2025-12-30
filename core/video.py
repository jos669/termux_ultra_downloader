import glob  # Para buscar archivos por patrón
import os
import subprocess
import time

from utils.colors import Colors
from utils.logger import log_message
from utils.path_manager import create_directories

from . import ffmpeg_utils  # Importar el nuevo módulo de utilidades de ffmpeg
from .downloader import run_yt_dlp
from .platforms import get_platform_name


def wait_for_file_creation(file_path, timeout=10):
    """
    Wait for a file to be fully created and written to disk.

    Args:
        file_path (str): Path to the file to wait for
        timeout (int): Maximum time to wait in seconds

    Returns:
        bool: True if file exists and is stable, False otherwise
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            # Check if file size is stable (not changing)
            initial_size = os.path.getsize(file_path)
            time.sleep(0.5)  # Wait a bit
            if os.path.exists(file_path) and os.path.getsize(file_path) == initial_size:
                return True
        time.sleep(0.5)
    return False


def download_video(
    url,
    quality,
    output_path,
    is_playlist,
    verbose,
    cookies_file,
    dry_run=False,
):
    """
    Función para descargar video desde YouTube con manejo de fusión de audio/video.

    Args:
        url (str): URL del video a descargar
        quality (str): Calidad del video (480p, 720p, 1080p, best)
        output_path (str): Ruta de salida para el archivo descargado
        is_playlist (bool): Indica si la URL es una playlist
        verbose (bool): Mostrar información detallada
        cookies_file (str): Ruta al archivo de cookies
        dry_run (bool): Modo de prueba sin descargar realmente

    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """

    platform = get_platform_name(url)
    is_short = "/shorts/" in url

    # Security validation: Check if output_path is safe to prevent directory traversal
    from .downloader import is_safe_path
    if not is_safe_path(os.path.expanduser("~"), output_path):
        print(f"{Colors.RED}ERROR: Ruta de salida insegura: {output_path}{Colors.RESET}")
        print(f"{Colors.YELLOW}La ruta de salida debe estar dentro del directorio de usuario para seguridad.{Colors.RESET}")
        return False

    if output_path == "/storage/emulated/0/Download" or output_path == "/data/data/com.termux/files/home/downloads":
        base_output_dir = output_path
    else:
        base_output_dir = os.path.join(output_path, platform, "video")

    # Validate and create directories safely
    if not create_directories(base_output_dir):
        print(f"{Colors.RED}ERROR: No se pudieron crear los directorios: {base_output_dir}{Colors.RESET}")
        return False

    # --- 1. Detección y verificación de FFmpeg ---
    ffmpeg_dir = ffmpeg_utils.get_ffmpeg_path()
    if not ffmpeg_dir or not ffmpeg_utils.check_ffmpeg(ffmpeg_dir):
        print(
            f"{Colors.RED}ERROR: FFmpeg no está disponible o no funciona. No se puede garantizar la fusión de audio/video.{Colors.RESET}"
        )
        return False

    # --- 2. Construcción de argumentos de yt-dlp ---
    temp_output_template = os.path.join(base_output_dir, "%(id)s.%(ext)s")

    if is_short:
        format_selector = "best[ext=mp4]/best"
    else:
        format_selector = "bv*+ba/b"

    base_args = [
        "--ignore-errors",
        "--continue",
        "--no-overwrites",
        "--merge-output-format",
        "mp4",
        "--ffmpeg-location",
        ffmpeg_dir,
        "-o",
        temp_output_template,
        "-f",
        format_selector,
    ]

    if not is_playlist:
        base_args.append("--no-playlist")
    else:
        print(
            f"{Colors.YELLOW}Descargando playlist. "
            f"Los archivos se guardarán en: {base_output_dir}"
            f"{Colors.RESET}"
        )

    # Argumentos de post-procesado
    if is_short:
        post_process_args = []
    else:
        post_process_args = ["--add-metadata", "--embed-thumbnail"]

    # --- 3. Intento de descarga inicial (con post-procesado) ---
    print(
        f"{Colors.YELLOW}Intentando descarga (con metadata/thumbnail)...{Colors.RESET}"
    )
    final_args_with_post = base_args + post_process_args

    initial_success = False
    try:
        run_yt_dlp(
            args=final_args_with_post,
            url=url,
            platform=platform,
            verbose=verbose,
            cookies_file=cookies_file,
            dry_run=dry_run,
        )
        initial_success = True
    except subprocess.CalledProcessError:
        print(
            f"{Colors.YELLOW}Descarga inicial falló con metadata/thumbnail.{Colors.RESET}"
        )
    if initial_success:
        print(f"{Colors.GREEN}Descarga y fusión inicial exitosa.{Colors.RESET}")
    else:
        print(
            f"{
                Colors.YELLOW}Reintentando sin metadata/thumbnail (problemas Android)...{
                Colors.RESET}"
        )
        final_args_no_post = base_args
        second_success = False
        try:
            run_yt_dlp(
                args=final_args_no_post,
                url=url,
                platform=platform,
                verbose=verbose,
                cookies_file=cookies_file,
                dry_run=dry_run,
            )
            second_success = True
        except subprocess.CalledProcessError:
            print(
                f"{Colors.RED}Segundo intento de descarga falló sin metadata/thumbnail.{Colors.RESET}"
            )

        if not second_success:
            print(f"{Colors.RED}Ambos intentos de descarga fallaron.{Colors.RESET}")
            # Solo intenta esto para videos que NO son shorts, ya que los shorts ya
            # tienen un formato simple
            print(
                f"{Colors.YELLOW}Tercer intento: Fallback a formato robusto (bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best)...{Colors.RESET}"
            )
            # Creamos una copia de base_args y reemplazamos el selector de formato
            robust_format_selector = (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            )
            third_attempt_args = []
            found_f_flag = False
            for arg in base_args:
                if arg == "-f":
                    third_attempt_args.append(arg)
                    third_attempt_args.append(robust_format_selector)
                    found_f_flag = True
                    continue
                if (
                    found_f_flag and arg == format_selector
                ):  # Skip the old format_selector after -f
                    found_f_flag = False
                    continue
                third_attempt_args.append(arg)

            third_success = False
            try:
                run_yt_dlp(
                    args=third_attempt_args,
                    url=url,
                    platform=platform,
                    verbose=verbose,
                    cookies_file=cookies_file,
                    dry_run=dry_run,
                )
                third_success = True
            except subprocess.CalledProcessError:
                print(
                    f"{Colors.RED}Tercer intento de descarga falló.{Colors.RESET}"
                )

            if not third_success:
                print(
                    f"{Colors.RED}Todos los intentos de descarga fallaron.{Colors.RESET}"
                )
                return False
    # --- 5. Búsqueda y Validación del Archivo Final ---
    print(
        f"{Colors.CYAN}Verificando archivos descargados y fusionados...{Colors.RESET}"
    )
    # Extraer ID de video de forma más robusta
    import re
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url.split('?')[0])
    if video_id_match:
        video_id_pattern = video_id_match.group(1)
    else:
        # Fallback: intentar obtener el último segmento de la URL
        video_id_pattern = url.split("/")[-1].split("?")[0]

    # Wait a bit for file system to settle after yt-dlp completes
    time.sleep(1)

    final_output_glob = os.path.join(base_output_dir, f"{video_id_pattern}*.mp4")
    final_merged_files = glob.glob(final_output_glob)

    actual_final_file = None
    if final_merged_files:
        # Wait for the file to be fully written to disk
        first_file = final_merged_files[0]
        if wait_for_file_creation(first_file):
            actual_final_file = first_file  # Tomar el primero que coincida
            print(
                f"{Colors.GREEN}[+] Archivo MP4 final encontrado: {actual_final_file}{Colors.RESET}"
            )
        else:
            print(
                f"{Colors.YELLOW}ADVERTENCIA: El archivo encontrado no está completamente escrito: {first_file}{Colors.RESET}")
    else:
        print(
            f"{
                Colors.YELLOW}ADVERTENCIA: No se encontró un archivo MP4 final usando el patrón '{video_id_pattern}'.{
                Colors.RESET}")
        # Podría ser un nombre diferente o yt-dlp no lo fusionó.
        # Buscaremos los componentes separados para el modo rescate.

    # --- 6. MODO RESCATE: Fusión manual si existen componentes separados ---
    video_glob = os.path.join(base_output_dir, f"{video_id_pattern}*.mp4")
    audio_glob_webm = os.path.join(base_output_dir, f"{video_id_pattern}*.webm")
    audio_glob_m4a = os.path.join(base_output_dir, f"{video_id_pattern}*.m4a")

    separate_video_files = glob.glob(video_glob)
    separate_audio_files = glob.glob(audio_glob_webm) + glob.glob(audio_glob_m4a)

    if separate_video_files and separate_audio_files and not actual_final_file:
        print(
            f"{Colors.RED}"
            "MODO RESCATE ACTIVADO 🔥: "
            "Video y audio detectados por separado. Fusionando..."
            f"{Colors.RESET}"
        )

        video_file = separate_video_files[0]
        audio_file = separate_audio_files[0]

        rescued_output = os.path.join(
            base_output_dir, f"{video_id_pattern}_RESCATADO.mp4"
        )

        rescue_cmd = [
            ffmpeg_dir,
            "-y",
            "-i",
            video_file,
            "-i",
            audio_file,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            rescued_output,
        ]

        try:
            subprocess.run(
                rescue_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            print(
                f"{Colors.GREEN}"
                "✔ FUSIÓN DE RESCATE COMPLETADA CON ÉXITO"
                f"{Colors.RESET}"
            )
            return True

        except subprocess.CalledProcessError:
            print(
                f"{Colors.RED}"
                "❌ ERROR: Falló la fusión manual con FFmpeg"
                f"{Colors.RESET}"
            )
            # Si falla la fusión directa, intentamos con la función de utilidad
            # Asumimos que el primer video y el primer audio son los correctos para
            # fusionar.
            video_component = separate_video_files[0]
            audio_component = separate_audio_files[0]

            # Nombre para el archivo fusionado manualmente
            manual_merged_filename = os.path.join(
                base_output_dir, f"{video_id_pattern}_merged.mp4"
            )

            if ffmpeg_utils.manual_merge_and_cleanup(
                video_component, audio_component, manual_merged_filename, ffmpeg_dir
            ):
                actual_final_file = manual_merged_filename
                print(
                    f"{Colors.GREEN}Fusión manual exitosa. Archivo final: {actual_final_file}{Colors.RESET}"
                )
            else:
                print(
                    f"{
                        Colors.RED}ERROR: La fusión manual falló. El video puede estar incompleto o sin audio.{
                        Colors.RESET}")
                return False

    # --- 7. Validación Final: Verificación de stream de audio ---
    if actual_final_file and ffmpeg_utils.has_audio_stream(
        actual_final_file, ffmpeg_dir
    ):
        print(
            f"{Colors.GREEN}¡Descarga de video con audio completada exitosamente!{Colors.RESET}"
        )
        return True
    elif actual_final_file:
        print(
            f"{
                Colors.RED}ADVERTENCIA: El archivo final '{actual_final_file}' no tiene stream de audio.{
                Colors.RESET}")
        log_message(
            f"ADVERTENCIA: Archivo final sin stream de audio: {actual_final_file}",
            "WARNING",
        )
        return False
    else:
        print(
            f"{Colors.RED}ERROR: No se pudo determinar el archivo final o está incompleto.{Colors.RESET}"
        )
        return False
