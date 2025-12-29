from core.audio import download_audio
from core.video import download_video


def download_playlist_video(
    url, quality, output_path, verbose, cookies_file, dry_run=False
):
    """Descarga una playlist de videos."""
    # is_playlist se establece en True dentro de download_video
    return download_video(
        url, quality, output_path, True, verbose, cookies_file, dry_run=dry_run
    )


def download_playlist_audio(
    url, format, bitrate, output_path, verbose, cookies_file, dry_run=False
):
    """Descarga una playlist de audios."""
    # is_playlist se establece en True dentro de download_audio
    return download_audio(
        url, output_path, format, bitrate, True, verbose, cookies_file, dry_run=dry_run
    )
