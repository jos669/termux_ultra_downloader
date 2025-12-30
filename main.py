import argparse
import os
import sys
import time  # Import the time module

from config import user_settings
from config.config_manager import get_default_path
# Importa el nuevo módulo downloader
from core import audio, batch, playlist, downloader
from ui import tui  # Importa el módulo tui completo
from ui.tui import get_random_urlvideo_logo  # Importar la nueva función de logo
from utils.path_manager import create_directories
from utils.validator import check_dependencies, update_yt_dlp

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def get_output_path_from_user():
    """
    Muestra la ruta de descarga predeterminada y pregunta al usuario si desea
    usarla o introducir una nueva.
    """
    default_path = get_default_path()
    print(f"La ruta de descarga predeterminada es: {default_path}")
    choice = input("¿Usar esta ruta? (s/n): ").lower()
    if choice == "s":
        return default_path
    else:
        new_path = input("Introduce la nueva ruta de descarga: ").strip()

        # Input validation
        if not new_path:
            print("Ruta vacía. Usando la predeterminada.")
            return default_path

        # Check for path traversal attempts
        if '..' in new_path or new_path.startswith('../') or '/..' in new_path:
            print("Ruta inválida: intento de navegación de directorios detectado. Usando la predeterminada.")
            return default_path

        # Normalize the path
        new_path = os.path.normpath(new_path)

        # Expand user home if needed
        if new_path.startswith('~'):
            new_path = os.path.expanduser(new_path)

        # Validate that the path is within safe boundaries
        from core.downloader import is_safe_path
        if not is_safe_path(os.path.expanduser("~"), new_path):
            print("Ruta inválida: fuera de los límites seguros. Usando la predeterminada.")
            return default_path

        if os.path.isdir(new_path):
            return new_path
        else:
            print(
                "La ruta introducida no es un directorio válido. Usando la predeterminada."
            )
            return default_path


def interactive_mode():
    main_menu_options = {
        "1": "Descargar Video",
        "2": "Descargar Solo Audio",
        "3": "Descargar Playlist",
        "4": "Descarga por Lotes (archivo.txt)",
        "5": "Configurar Ruta de Descarga Predeterminada",
        "6": "Actualizar yt-dlp",
        "0": "Salir",
    }
    valid_choices = list(main_menu_options.keys())

    while True:
        tui.print_dashboard()
        time.sleep(2)
        tui.display_main_menu(
            main_menu_options,
            urlvideo_logo=get_random_urlvideo_logo(),
        )
        choice = tui.get_menu_choice(valid_choices)

        if choice == "1":
            # Descargar Video y Audio Fusionados (Lógica nueva y corregida)
            while True:
                url = input("Introduce la URL del video (o 'm' para volver al menú): ")
                if url.lower() == 'm':
                    break
                output_path = get_output_path_from_user()
                final_file = downloader.download_and_merge_video_audio(
                    url,
                    output_path=output_path,
                    verbose=False,
                    cookies_file=None,
                )
                if final_file and os.path.exists(final_file):
                    print(f"\n✅ ¡Éxito! Archivo guardado en: {final_file}")
                else:
                    print("\n❌ La descarga y fusión fallaron. Revisa los logs para más detalles.")

                another = input("¿Descargar otro video? (s/n): ").lower()
                if another != 's':
                    break

        elif choice == "2":
            # Descargar Solo Audio
            while True:
                url = input("Introduce la URL del audio (o 'm' para volver al menú): ")
                if url.lower() == 'm':
                    break
                output_path = get_output_path_from_user()
                audio.download_audio(
                    url,
                    output_path,
                    format="mp3",
                    bitrate="best",
                    is_playlist=False,
                    verbose=False,
                    cookies_file=None,
                )
                another = input("¿Descargar otro audio? (s/n): ").lower()
                if another != 's':
                    break

        elif choice == "3":
            # Playlist Downloader
            while True:
                url = input(
                    "Introduce la URL de la playlist (o 'm' para volver al menú): ")
                if url.lower() == 'm':
                    break
                output_path = get_output_path_from_user()
                playlist_choice = input(
                    "¿Descargar como video o audio? (v/a): ").lower()
                if playlist_choice == "v":
                    # Para playlists de video, ahora usamos la nueva función de fusión
                    # para cada video
                    print("Iniciando descarga de playlist como videos fusionados...")
                    playlist.download_playlist_video(
                        url,
                        quality="best",
                        output_path=output_path,
                        verbose=False,
                        cookies_file=None,
                    )
                elif playlist_choice == "a":
                    playlist.download_playlist_audio(
                        url,
                        format="mp3",
                        bitrate="best",
                        output_path=output_path,
                        verbose=False,
                        cookies_file=None,
                    )
                else:
                    print("Opción no válida.")

                another = input("¿Descargar otra playlist? (s/n): ").lower()
                if another != 's':
                    break

        elif choice == "4":
            # Batch Downloader
            while True:
                file_path = input(
                    "Introduce la ruta del archivo con URLs (o 'm' para volver al menú): ")
                if file_path.lower() == 'm':
                    break
                output_path = get_output_path_from_user()
                media_type = input("¿Descargar como video o audio? (v/a): ").lower()
                if media_type == "v":
                    media_type = "video"
                    config_option = "best"  # Usamos la mejor calidad por defecto con la nueva lógica
                elif media_type == "a":
                    media_type = "audio"
                    config_option = input(
                        "Introduce el formato de audio (e.g., mp3, wav): "
                    )
                else:
                    print("Opción de media no válida.")
                    continue

                batch.process_batch_download(
                    file_path,
                    output_path,
                    media_type,
                    config_option,
                    verbose=False,
                    cookies_file=None,
                )
                another = input("¿Procesar otro archivo de lotes? (s/n): ").lower()
                if another != 's':
                    break

        elif choice == "5":
            # Configurar Ruta de Descarga Predeterminada
            new_default_path = input(
                "Introduce la nueva ruta de descarga predeterminada: "
            )
            if os.path.isdir(new_default_path):
                user_settings.set_default_path(new_default_path)
            else:
                print("La ruta introducida no es un directorio válido.")

        elif choice == "6":
            update_yt_dlp()

        elif choice == "0":
            print("Saliendo del programa.")
            break

        # Dar tiempo al usuario para ver los resultados antes de limpiar la pantalla
        # input("\nPresiona Enter para continuar...")


def main():
    parser = argparse.ArgumentParser(description="Termux Ultra Downloader (TUD)")
    subparsers = parser.add_subparsers(dest="command")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Verifica dependencias e " "instala carpetas.")

    # Video command
    video_parser = subparsers.add_parser("video", help="Descargar videos")
    video_parser.add_argument("quality", choices=["best", "1080p", "720p", "480p"], help="Calidad del video")
    video_parser.add_argument("url", help="URL del video")
    video_parser.add_argument("--route", dest="output_path", default=get_default_path(), help="Ruta de salida para la descarga")
    video_parser.add_argument("--cookies", dest="cookies_file", help="Ruta al archivo de cookies")

    # Audio command
    audio_parser = subparsers.add_parser("audio", help="Descargar audio")
    audio_parser.add_argument("format", choices=["mp3", "m4a", "flac", "wav"], help="Formato de audio")
    audio_parser.add_argument("bitrate", choices=["best", "320", "192", "128"], help="Bitrate del audio")
    audio_parser.add_argument("url", help="URL del video/audio")
    audio_parser.add_argument("--route", dest="output_path", default=get_default_path(), help="Ruta de salida para la descarga")
    audio_parser.add_argument("--cookies", dest="cookies_file", help="Ruta al archivo de cookies")

    # Playlist command
    playlist_parser = subparsers.add_parser("playlist", help="Descargar playlist")
    playlist_parser.add_argument("media_type", choices=["video", "audio"], help="Tipo de media")
    playlist_parser.add_argument("quality", help="Calidad del video o formato del audio")
    playlist_parser.add_argument("url", help="URL de la playlist")
    playlist_parser.add_argument("--route", dest="output_path", default=get_default_path(), help="Ruta de salida para la descarga")
    playlist_parser.add_argument("--cookies", dest="cookies_file", help="Ruta al archivo de cookies")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Descarga masiva desde archivo")
    batch_parser.add_argument("media_type", choices=["video", "audio"], help="Tipo de media")
    batch_parser.add_argument("config_option", help="Calidad de video o formato de audio")
    batch_parser.add_argument("file_path", help="Ruta al archivo con URLs")
    batch_parser.add_argument("--route", dest="output_path", default=get_default_path(), help="Ruta de salida para la descarga")
    batch_parser.add_argument("--cookies", dest="cookies_file", help="Ruta al archivo de cookies")

    if len(sys.argv) == 1:
        check_dependencies()
        create_directories(get_default_path())
        interactive_mode()
        return

    args = parser.parse_args()

    if args.command == "setup":
        print("Ejecutando setup...")
        check_dependencies()
        create_directories(get_default_path())
        print("¡Setup completado exitosamente!")
    elif args.command == "video":
        print(f"Descargando video desde: {args.url}")
        result = downloader.download_and_merge_video_audio(
            args.url,
            output_path=args.output_path,
            verbose=True,
            cookies_file=args.cookies_file
        )
        if result:
            print(f"✅ Video descargado exitosamente: {result}")
        else:
            print("❌ Falló la descarga del video")
    elif args.command == "audio":
        print(f"Descargando audio desde: {args.url}")
        success = audio.download_audio(
            args.url,
            output_path=args.output_path,
            format=args.format,
            bitrate="best" if args.bitrate == "best" else args.bitrate + "K",
            is_playlist=False,
            verbose=True,
            cookies_file=args.cookies_file
        )
        if success:
            print("✅ Audio descargado exitosamente")
        else:
            print("❌ Falló la descarga del audio")
    elif args.command == "playlist":
        print(f"Descargando playlist desde: {args.url}")
        if args.media_type == "video":
            playlist.download_playlist_video(
                args.url,
                quality=args.quality,
                output_path=args.output_path,
                verbose=True,
                cookies_file=args.cookies_file
            )
        else:  # audio
            playlist.download_playlist_audio(
                args.url,
                format=args.quality,  # For audio, quality parameter is the format
                bitrate="best",
                output_path=args.output_path,
                verbose=True,
                cookies_file=args.cookies_file
            )
        print("✅ Playlist descargada exitosamente")
    elif args.command == "batch":
        print(f"Descargando en batch desde archivo: {args.file_path}")
        batch.process_batch_download(
            args.file_path,
            output_path=args.output_path,
            media_type=args.media_type,
            config_option=args.config_option,
            verbose=True,
            cookies_file=args.cookies_file
        )
        print("✅ Descarga batch completada")
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
