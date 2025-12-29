import os
import subprocess
import shutil
import hashlib
from urllib.parse import urlparse

from utils.colors import Colors
from utils.logger import log_message

# --- Rutas de binarios (gestionadas con shutil.which para robustez en Termux) ---
YT_DLP_PATH = shutil.which("yt-dlp")
FFMPEG_PATH = shutil.which("ffmpeg")  # yt-dlp lo necesitará para la fusión


def get_video_filename(url: str) -> str:
    """Genera un nombre de archivo base seguro para la URL."""
    # Simplifica el nombre del archivo para evitar caracteres especiales
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.hostname or "youtu.be" in parsed_url.hostname:
        if "v=" in parsed_url.query:
            video_id = parsed_url.query.split("v=")[1].split("&")[0]
            return f"youtube_{video_id}"
        elif parsed_url.path and parsed_url.path != '/':
            video_id = parsed_url.path.strip('/').split('/')[-1]
            return f"youtube_{video_id}"

    # Para otras URLs, un nombre más genérico o basado en el hash
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:10]
    return f"media_{url_hash}"


def download_and_merge_video_audio(
        url: str,
        output_path: str,
        verbose: bool = False,
        cookies_file: str = None) -> str | None:
    """
    Descarga el video y el audio de forma separada y los fusiona usando yt-dlp
    (que internamente llama a ffmpeg para la fusión).
    Retorna la ruta del archivo final si tiene éxito, None en caso contrario.
    """
    if not YT_DLP_PATH:
        print(
            f"{Colors.RED}ERROR: 'yt-dlp' no encontrado. Asegúrate de que está instalado.{Colors.RESET}")
        return None
    if not FFMPEG_PATH:
        print(f"{Colors.RED}ERROR: 'ffmpeg' no encontrado. yt-dlp lo necesita para fusionar video/audio.{Colors.RESET}")
        return None

    if not os.access(os.path.dirname(output_path) or output_path, os.W_OK):
        print(f"{Colors.RED}ERROR: No se tienen permisos de escritura para la ruta: {output_path}{Colors.RESET}")
        print(f"{Colors.YELLOW}Por favor, ejecuta 'termux-setup-storage' en tu terminal, concede los permisos y reinicia Termux.{Colors.RESET}")
        return None

    os.makedirs(output_path, exist_ok=True)

    base_filename = get_video_filename(url)
    output_template = os.path.join(output_path, f"{base_filename}.%(ext)s")

    # Comando de yt-dlp para descargar mejor video y mejor audio y fusionarlos en MP4
    args = [
        "-f", "bestvideo+bestaudio/best",  # Selecciona el mejor video y audio, fallback a 'best'
        "--merge-output-format", "mp4",   # Fusiona los streams en un archivo MP4
        "--no-warnings",                  # Oculta advertencias no críticas
        "--restrict-filenames",           # Crea nombres de archivo seguros
        "-o", output_template,            # Define la plantilla de salida
    ]

    try:
        process = run_yt_dlp(
            args,
            url,
            "general",
            verbose=verbose,
            cookies_file=cookies_file)

        if process.returncode == 0:
            # yt-dlp imprime el nombre del archivo final en stdout/stderr al finalizar
            # la fusión
            output_lines = (process.stdout + process.stderr).splitlines()
            for line in reversed(output_lines):  # Buscamos desde el final
                if "Destination:" in line and "mp4" in line:
                    try:
                        # Extraer el nombre de archivo de la línea de destino
                        parts = line.split("Destination: ")
                        if len(parts) > 1:
                            downloaded_filename = parts[1].strip()
                            full_path = os.path.join(output_path, downloaded_filename)
                            if os.path.exists(full_path):
                                return full_path
                    except Exception:
                        pass  # Si hay error al parsear, ignorar y seguir buscando

            # Fallback: Si no encontramos el "Destination:", intentamos con el output_template
            # yt-dlp casi siempre pondrá mp4 cuando se usa --merge-output-format mp4
            final_filepath_guess = os.path.join(output_path, f"{base_filename}.mp4")
            if os.path.exists(final_filepath_guess):
                return final_filepath_guess

            print(
                f"{Colors.YELLOW}[ADVERTENCIA] No se pudo determinar la ruta exacta del archivo final, pero yt-dlp reportó éxito.{Colors.RESET}")
            return None  # No se pudo verificar el archivo, pero yt-dlp dijo que sí
        else:
            print(
                f"{
                    Colors.RED}[FALLO] La descarga y fusión de yt-dlp falló con código de salida {
                    process.returncode}.{
                    Colors.RESET}")
            return None
    except Exception as e:
        print(f"{Colors.RED}ERROR inesperado durante la descarga y fusión: {e}{Colors.RESET}")
        return None


def run_yt_dlp(
    args,
    url,
    platform,
    verbose=False,  # Añadido
    cookies_file=None,
    dry_run=False,  # Añadido
):
    """
    Ejecuta un comando de yt-dlp y captura su salida.
    Retorna el objeto CompletedProcess.
    Eleva subprocess.CalledProcessError si el comando falla (check=True).
    """
    command = ["yt-dlp"] + args
    if cookies_file:
        command.extend(["--cookies", cookies_file])
    command.append(url)  # La URL siempre al final

    # Mostrar el comando que se va a ejecutar (para depuración y transparencia)
    full_command_str = " ".join(command)
    print(
        f"{Colors.CYAN}=================================================={Colors.RESET}"
    )
    print(f"{Colors.BOLD}{Colors.YELLOW}Iniciando operación...{Colors.RESET}")
    print(f"{Colors.CYAN}URL: {url}{Colors.RESET}")
    print(f"{Colors.CYAN}Comando yt-dlp: {full_command_str}{Colors.RESET}")
    print(
        f"{Colors.CYAN}=================================================={Colors.RESET}\n"
    )

    log_message(f"Ejecutando yt-dlp: {full_command_str}", "INFO", url, platform)

    try:
        # --- Construcción del Entorno de Termux ---
        # Esto es CRÍTICO. Un subproceso no hereda el entorno de un shell
        # interactivo (como fish o bash), causando fallos silenciosos.
        env = os.environ.copy()

        # PREFIX es la variable más importante de Termux, todo se basa en ella.
        prefix = env.get('PREFIX')
        if not prefix:
            # Fallback por si no estuviera, aunque es muy raro.
            prefix = '/data/data/com.termux/files/usr'

        # 1. LD_LIBRARY_PATH: La causa más probable de fallos silenciosos.
        #    Le dice al sistema dónde encontrar las librerías compartidas (.so).
        env['LD_LIBRARY_PATH'] = f"{prefix}/lib"

        # 2. HOME: Necesario para que yt-dlp encuentre su config, cache, etc.
        env['HOME'] = os.path.expanduser('~')

        # 3. PATH: Asegura que todos los binarios de Termux sean encontrables.
        env['PATH'] = f"{prefix}/bin:{env.get('PATH', '')}"

        # 4. TMPDIR: Ubicación para archivos temporales.
        env['TMPDIR'] = f"{prefix}/tmp"

        # --- Ejecución del Proceso ---
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            env=env  # Usar el entorno recién construido
        )
        return process
    except subprocess.CalledProcessError as e:
        log_message(
            f"yt-dlp falló con código {e.returncode}. STDOUT: {e.stdout}, STDERR: {e.stderr}",
            "ERROR",
            url,
            platform,
        )
        raise  # Re-lanzar la excepción para que sea manejada por el llamador
    except FileNotFoundError:
        print(
            f"{Colors.RED}ERROR: 'yt-dlp' no encontrado. Asegúrate de que está en el PATH.{Colors.RESET}"
        )
        log_message("ERROR: yt-dlp no encontrado.", "ERROR", url, platform)
        raise
    except Exception as e:
        print(
            f"{Colors.RED}Un error inesperado al ejecutar yt-dlp ha ocurrido: {e}{Colors.RESET}"
        )
        log_message(f"Error inesperado al ejecutar yt-dlp: {e}", "ERROR", url, platform)
        raise
