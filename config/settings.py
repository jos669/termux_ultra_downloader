import os

# ---[ RUTA DE DESCARGA PREDETERMINADA ]-------------------------------------
# Esta es la ruta por defecto. Se creará dentro del directorio del proyecto.
# Puede ser modificada por el usuario a través de la aplicación.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_BASE_DIR = "/data/data/com.termux/files/home/downloads"

# ---[ RUTAS DE LOGS ]-------------------------------------------------------
# Los logs también se guardarán dentro de la carpeta de descargas del proyecto.
LOGS_DIR = os.path.join(DOWNLOADS_BASE_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "downloader.log")

# ---[ CONFIGURACIÓN DE DESCARGA ]-------------------------------------------

# Calidades de video disponibles
VIDEO_QUALITY_MAP = {
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "best": "bestvideo+bestaudio/best",
}

# Formatos de audio disponibles
AUDIO_FORMAT_MAP = {"mp3": "mp3", "m4a": "m4a", "flac": "flac", "wav": "wav"}

# Calidades de audio disponibles (para formatos con pérdida)
AUDIO_QUALITY_MAP = {
    "128": "128K",
    "192": "192K",
    "320": "320K",
    "best": "0",  # 0 es la mejor calidad en yt-dlp
}
