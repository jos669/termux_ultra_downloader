from config.settings import AUDIO_FORMAT_MAP, VIDEO_QUALITY_MAP
from core.audio import download_audio
from core.video import download_video
from utils.colors import Colors
from utils.logger import log_message
from utils.path_manager import create_directories


def process_batch_download(
    file_path,
    output_path,
    media_type,
    config_option,
    verbose,
    cookies_file,
    dry_run=False,
):
    """Descarga masiva desde un archivo de texto."""
    try:
        # Asegurarse de que el directorio de salida exista
        create_directories(output_path)

        with open(file_path, encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(
            f"{Colors.RED}Error: El archivo '{file_path}' no fue "
            f"encontrado.{Colors.RESET}"
        )
        log_message(f"Archivo para batch no encontrado: {file_path}", "ERROR")
        return

    if not urls:
        print(
            f"{Colors.YELLOW}El archivo está vacío o no contiene URLs "
            f"válidas.{Colors.RESET}"
        )
        return

    print(
        f"{Colors.GREEN}Se encontraron {len(urls)} URLs en el archivo."
        f"{Colors.RESET}"
    )
    log_message(
        f"Iniciando descarga masiva de {len(urls)} URLs desde " f"'{file_path}'."
    )

    # Validar opciones de configuración para batch
    if media_type == "video":
        if config_option not in VIDEO_QUALITY_MAP:
            print(
                f"{Colors.RED}Error: Calidad de video '{config_option}' no "
                f"válida para batch. Opciones: "
                f"{list(VIDEO_QUALITY_MAP.keys())}{Colors.RESET}"
            )
            return
    elif media_type == "audio":
        # Asumiendo que config_option es el formato para audio
        if config_option not in AUDIO_FORMAT_MAP:
            print(
                f"{Colors.RED}Error: Formato de audio '{config_option}' no "
                f"válido para batch. Opciones: "
                f"{list(AUDIO_FORMAT_MAP.keys())}{Colors.RESET}"
            )
            return

    for i, url in enumerate(urls, 1):
        print(
            f"\n{Colors.BOLD}{Colors.MAGENTA}Procesando URL {i}/{len(urls)}: "
            f"{url}{Colors.RESET}"
        )
        if media_type == "video":
            download_video(
                url,
                quality=config_option,
                output_path=output_path,
                is_playlist=False,
                verbose=verbose,
                cookies_file=cookies_file,
                dry_run=dry_run,
            )
        elif media_type == "audio":
            download_audio(
                url,
                output_path=output_path,
                format=config_option,
                bitrate="best",
                is_playlist=False,
                verbose=verbose,
                cookies_file=cookies_file,
                dry_run=dry_run,
            )
