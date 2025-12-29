import argparse
import os
import sys
import time  # Import the time module

from config import user_settings
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
    default_path = user_settings.get_default_path()
    print(f"La ruta de descarga predeterminada es: {default_path}")
    choice = input("¿Usar esta ruta? (s/n): ").lower()
    if choice == "s":
        return default_path
    else:
        new_path = input("Introduce la nueva ruta de descarga: ")
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
    subparsers.add_parser("setup", help="Verifica dependencias e " "instala carpetas.")

    if len(sys.argv) == 1:
        check_dependencies()
        create_directories(user_settings.get_default_path())
        interactive_mode()
        return

    args = parser.parse_args()

    if args.command == "setup":
        print("Ejecutando setup...")
        check_dependencies()
        create_directories(user_settings.get_default_path())
        print("¡Setup completado exitosamente!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
