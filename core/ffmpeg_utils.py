import os
import shutil
import subprocess

from utils.colors import Colors
from utils.logger import log_message


def get_ffmpeg_path():
    """
    Busca el ejecutable de ffmpeg/ffprobe en el PATH.
    Retorna la ruta al directorio que contiene los binarios si los encuentra, None en caso contrario.
    """
    ffmpeg_exec = shutil.which("ffmpeg")
    ffprobe_exec = shutil.which("ffprobe")

    if ffmpeg_exec and ffprobe_exec:
        ffmpeg_dir = os.path.dirname(ffmpeg_exec)
        log_message(f"FFmpeg/FFprobe detectado en: {ffmpeg_dir}", "INFO")
        return ffmpeg_dir
    else:
        log_message("FFmpeg o FFprobe no encontrados en el PATH.", "WARNING")
        return None


def check_ffmpeg(ffmpeg_dir):
    """
    Verifica que ffmpeg sea ejecutable y funcione correctamente.
    Retorna True si es válido, False en caso contrario.
    """
    if not ffmpeg_dir:
        print(
            f"{Colors.RED}ERROR: No se proporcionó ruta de FFmpeg para verificar.{Colors.RESET}"
        )
        log_message("ERROR: No se proporcionó ruta de FFmpeg para verificar.", "ERROR")
        return False

    ffmpeg_exec_path = os.path.join(ffmpeg_dir, "ffmpeg")

    try:
        process = subprocess.run(
            [ffmpeg_exec_path, "-version"],
            capture_output=True,
            text=True,
            check=False,  # No queremos que lance excepción si -version falla por alguna razón
            encoding="utf-8",
        )
        if process.returncode == 0:
            print(
                f"{Colors.GREEN}[+] FFmpeg verificado y funcional en: {ffmpeg_dir}{Colors.RESET}"
            )
            log_message(f"FFmpeg verificado: {ffmpeg_dir}", "INFO")
            return True
        else:
            print(
                f"{
                    Colors.RED}ERROR: FFmpeg encontrado pero falló la verificación: {
                    process.stderr}{
                    Colors.RESET}"
            )
            log_message(
                f"ERROR: FFmpeg falló la verificación: {
                    process.stderr}",
                "ERROR",
            )
            return False
    except FileNotFoundError:
        print(
            f"{Colors.RED}ERROR: FFmpeg no encontrado en la ruta especificada: {ffmpeg_dir}{Colors.RESET}"
        )
        log_message(f"ERROR: FFmpeg no encontrado en: {ffmpeg_dir}", "ERROR")
        return False
    except Exception as e:
        print(f"{Colors.RED}ERROR inesperado al verificar FFmpeg: {e}{Colors.RESET}")
        log_message(f"ERROR inesperado al verificar FFmpeg: {e}", "ERROR")
        return False


def manual_merge_and_cleanup(video_file, audio_file, output_file, ffmpeg_dir):
    """
    Fusiona video y audio manualmente usando ffmpeg.
    Elimina los archivos de entrada (video_file, audio_file) si la fusión es exitosa.
    """
    if not os.path.exists(video_file):
        print(
            f"{Colors.RED}ERROR: Archivo de video no encontrado para fusión manual: {video_file}{Colors.RESET}"
        )
        log_message(
            f"ERROR: Archivo de video no encontrado para fusión manual: {video_file}",
            "ERROR",
        )
        return False
    if not os.path.exists(audio_file):
        print(
            f"{Colors.RED}ERROR: Archivo de audio no encontrado para fusión manual: {audio_file}{Colors.RESET}"
        )
        log_message(
            f"ERROR: Archivo de audio no encontrado para fusión manual: {audio_file}",
            "ERROR",
        )
        return False

    ffmpeg_exec_path = os.path.join(ffmpeg_dir, "ffmpeg")
    command = [
        ffmpeg_exec_path,
        "-y",  # Sobrescribir archivo de salida sin preguntar
        "-i",
        video_file,
        "-i",
        audio_file,
        "-c",
        "copy",  # Copiar streams sin recodificar para mayor velocidad
        output_file,
    ]

    print(f"\n{Colors.YELLOW}Iniciando fusión manual de video y audio...{Colors.RESET}")
    log_message(f"Comando de fusión manual: {' '.join(command)}", "INFO")

    try:
        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding="utf-8"
        )
        if process.returncode == 0:
            print(
                f"{Colors.GREEN}[+] Fusión manual completada con éxito en: {output_file}{Colors.RESET}"
            )
            log_message(f"Fusión manual exitosa: {output_file}", "SUCCESS")
            # Eliminar archivos originales solo si la fusión fue exitosa
            try:
                os.remove(video_file)
                os.remove(audio_file)
                print(
                    f"{Colors.GREEN}[+] Archivos temporales eliminados: {video_file}, {audio_file}{Colors.RESET}"
                )
                log_message(
                    f"Archivos temporales eliminados: {video_file}, {audio_file}",
                    "INFO",
                )
            except OSError as e:
                print(
                    f"{Colors.RED}ADVERTENCIA: No se pudieron eliminar archivos temporales: {e}{Colors.RESET}"
                )
                log_message(
                    f"ADVERTENCIA: No se pudieron eliminar archivos temporales: {e}",
                    "WARNING",
                )
            return True
        else:
            print(
                f"{
                    Colors.RED}ERROR: Fusión manual falló. Código: {
                    process.returncode}. Mensaje: {
                    process.stderr}{
                    Colors.RESET}"
            )
            log_message(
                f"ERROR: Fusión manual falló. Salida: {
                    process.stderr}",
                "ERROR",
            )
            return False
    except FileNotFoundError:
        print(
            f"{Colors.RED}ERROR: FFmpeg no encontrado para la fusión manual. Asegúrate de que '{ffmpeg_dir}' es la ruta correcta.{Colors.RESET}"
        )
        log_message(
            f"ERROR: FFmpeg no encontrado para fusión manual en: {ffmpeg_dir}", "ERROR"
        )
        return False
    except Exception as e:
        print(
            f"{Colors.RED}ERROR inesperado durante la fusión manual: {e}{Colors.RESET}"
        )
        log_message(f"ERROR inesperado durante la fusión manual: {e}", "ERROR")
        return False


def has_audio_stream(file_path, ffmpeg_dir):
    """
    Verifica si un archivo de video tiene un stream de audio usando ffprobe.
    Retorna True si tiene audio, False en caso contrario o si ffprobe falla.
    """
    if not os.path.exists(file_path):
        print(
            f"{Colors.RED}ERROR: Archivo no encontrado para verificar stream de audio: {file_path}{Colors.RESET}"
        )
        log_message(
            f"ERROR: Archivo no encontrado para verificar audio: {file_path}", "ERROR"
        )
        return False

    ffprobe_exec_path = os.path.join(ffmpeg_dir, "ffprobe")
    command = [
        ffprobe_exec_path,
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]

    log_message(f"Comando ffprobe para verificar audio: {' '.join(command)}", "INFO")
    try:
        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding="utf-8"
        )
        if process.returncode == 0 and "audio" in process.stdout.strip():
            print(
                f"{Colors.GREEN}[+] Archivo '{file_path}' contiene stream de audio.{Colors.RESET}"
            )
            log_message(f"Archivo '{file_path}' contiene stream de audio.", "INFO")
            return True
        else:
            print(
                f"{
                    Colors.YELLOW}ADVERTENCIA: Archivo '{file_path}' NO contiene stream de audio o ffprobe falló: {
                    process.stderr}{
                    Colors.RESET}")
            log_message(
                f"Archivo '{file_path}' NO contiene stream de audio o ffprobe falló: {
                    process.stderr}",
                "WARNING",
            )
            return False
    except FileNotFoundError:
        print(
            f"{
                Colors.RED}ERROR: ffprobe no encontrado. Asegúrate de que '{ffmpeg_dir}' es la ruta correcta.{
                Colors.RESET}")
        log_message(f"ERROR: ffprobe no encontrado en: {ffmpeg_dir}", "ERROR")
        return False
    except Exception as e:
        print(
            f"{Colors.RED}ERROR inesperado al verificar stream de audio: {e}{Colors.RESET}"
        )
        log_message(f"ERROR inesperado al verificar stream de audio: {e}", "ERROR")
        return False
