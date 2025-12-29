#!/usr/bin/env python3
import os
import subprocess
import sys

print("--- INICIANDO SCRIPT DE DEPURACIÓN DE YT-DLP ---")

# --- 1. Replicar el comando exacto que falla ---
# Usamos el comando del "tercer intento" que es el más robusto.
URL = "https://youtube.com/shorts/MVFt1DaduIk?si=rPU2L5khvzdjTqg1"
ffmpeg_location = "/data/data/com.termux/files/usr/bin"  # Directorio que contiene ffmpeg
output_template = "/storage/emulated/0/Download/%(id)s.%(ext)s"
format_selector = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

command = [
    "yt-dlp",
    "--ignore-errors",
    "--verbose",  # Añadimos --verbose para obtener la máxima información
    "--continue",
    "--no-overwrites",
    "--merge-output-format", "mp4",
    "--ffmpeg-location", ffmpeg_location,
    "-o", output_template,
    "-f", format_selector,
    "--no-playlist",
    URL
]

print(f"\n[INFO] Comando a ejecutar:\n{' '.join(command)}\n")


# --- 2. Replicar el entorno exacto de Termux ---
# Esta es la parte más crítica.
try:
    env = os.environ.copy()
    prefix = env.get('PREFIX', '/data/data/com.termux/files/usr')

    env['LD_LIBRARY_PATH'] = f"{prefix}/lib"
    env['HOME'] = os.path.expanduser('~')
    env['PATH'] = f"{prefix}/bin:" + env.get('PATH', '')
    env['TMPDIR'] = f"{prefix}/tmp"

    print("[INFO] Entorno para el subproceso:")
    print(f"  HOME = {env.get('HOME')}")
    print(f"  PATH = {env.get('PATH')}")
    print(f"  LD_LIBRARY_PATH = {env.get('LD_LIBRARY_PATH')}")
    print(f"  TMPDIR = {env.get('TMPDIR')}")
    print("-" * 20)

except Exception as e:
    print(f"\n[ERROR] Fallo al construir el entorno: {e}")
    sys.exit(1)


# --- 3. Ejecutar el comando ---
# NOTA IMPORTANTE: No usamos 'capture_output=True'.
# Dejamos que stdout y stderr se impriman directamente en la terminal.
# Esto es esencial para capturar errores de bajo nivel que 'capture_output' puede ocultar.
try:
    print("\n[INFO] Intentando ejecutar yt-dlp...")
    # Ejecutamos el proceso con el entorno adecuado
    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    print("\n--- FINALIZADO ---")
    print(f"Código de salida de yt-dlp: {result.returncode}")

    # Mostrar la salida estándar si existe
    if result.stdout:
        print(f"[yt-dlp STDOUT]\n{result.stdout}")

    # Mostrar la salida de error si existe
    if result.stderr:
        print(f"[yt-dlp STDERR]\n{result.stderr}")

    if result.returncode != 0:
        print("\n[FALLO] El proceso de yt-dlp terminó con un error.")
    else:
        print("\n[ÉXITO] El proceso de yt-dlp terminó correctamente.")

except FileNotFoundError:
    print("\n[ERROR CRÍTICO] 'yt-dlp' no se encontró. El PATH podría ser incorrecto.")
except Exception as e:
    print(f"\n[ERROR CRÍTICO] Una excepción ocurrió al intentar ejecutar el proceso: {e}")
