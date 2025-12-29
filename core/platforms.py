# (Sin cambios)
import re


def get_platform_name(url):
    """Detecta la plataforma a partir de una URL."""
    if re.search(r"youtube\.com|youtu\.be", url):
        return "YouTube"
    if re.search(r"tiktok\.com", url):
        return "TikTok"
    if re.search(r"facebook\.com|fb\.watch", url):
        return "Facebook"
    if re.search(r"instagram\.com", url):
        return "Instagram"
    if re.search(r"twitter\.com|x\.com", url):
        return "Twitter-X"
    return "Generic"
