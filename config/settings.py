import os

# ---[ RUTA DE DESCARGA PREDETERMINADA ]-------------------------------------
# Esta es la ruta por defecto. Se creará dentro del directorio del proyecto.
# Puede ser modificada por el usuario a través de la aplicación.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Detectar ruta de descargas de forma más segura
def get_default_downloads_path():
    """Obtiene la ruta predeterminada de descargas de forma segura."""
    # Primero intenta con la ruta de descargas estándar de Termux
    termux_storage = os.path.expanduser("~/storage/downloads")
    if os.path.exists(termux_storage):
        return termux_storage

    # Si no existe, intenta crear una carpeta en el directorio home
    home_downloads = os.path.expanduser("~/downloads")
    try:
        os.makedirs(home_downloads, exist_ok=True)
        return home_downloads
    except (PermissionError, OSError):
        # Si no se puede crear, usar el directorio actual
        return os.getcwd()

# ---[ RUTAS DE LOGS ]-------------------------------------------------------
# Los logs también se guardarán dentro de la carpeta de descargas del proyecto.
# These will be updated dynamically based on the user's config
def get_logs_dir():
    from .config_manager import get_default_path
    return os.path.join(get_default_path(), "logs")

def get_log_file():
    return os.path.join(get_logs_dir(), "downloader.log")

# ---[ CONFIGURACIÓN DE DESCARGA ]-------------------------------------------

def get_video_quality_map():
    """Obtiene el mapeo de calidades de video desde la configuración."""
    from .config_manager import get_config_value
    return get_config_value("video_quality_map", {
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "best": "bestvideo+bestaudio/best",
    })

def get_audio_format_map():
    """Obtiene el mapeo de formatos de audio desde la configuración."""
    from .config_manager import get_config_value
    return get_config_value("audio_format_map", {
        "mp3": "mp3", "m4a": "m4a", "flac": "flac", "wav": "wav"
    })

def get_audio_quality_map():
    """Obtiene el mapeo de calidades de audio desde la configuración."""
    from .config_manager import get_config_value
    return get_config_value("audio_quality_map", {
        "128": "128K",
        "192": "192K",
        "320": "320K",
        "best": "0",  # 0 es la mejor calidad en yt-dlp
    })

# Calidades de video disponibles (usando la función configurable)
def get_video_quality(quality):
    """Obtiene la calidad de video específica."""
    return get_video_quality_map().get(quality)

# Formatos de audio disponibles (usando la función configurable)
def get_audio_format(format_name):
    """Obtiene el formato de audio específico."""
    return get_audio_format_map().get(format_name)

# Calidades de audio disponibles (usando la función configurable)
def get_audio_quality(quality):
    """Obtiene la calidad de audio específica."""
    return get_audio_quality_map().get(quality)
