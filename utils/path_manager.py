import os
import shutil
import sys

from config import config_manager

from .colors import Colors


def get_user_input(prompt):
    """
    Obtiene una entrada del usuario y maneja la salida del programa.

    Args:
        prompt (str): Mensaje a mostrar al usuario

    Returns:
        str: Entrada del usuario o sale del programa si se cancela
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{Colors.YELLOW}Operación cancelada. Saliendo..." f"{Colors.RESET}")
        sys.exit(0)


def create_directories(path):
    """
    Crea las carpetas de destino si no existen.

    Args:
        path (str): Ruta del directorio a crear

    Returns:
        bool: True si se creó exitosamente, False en caso contrario
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except PermissionError:
        print(
            f"{Colors.RED}Error de permisos al crear el directorio '{path}'. "
            f"Ejecuta 'termux-setup-storage' y otorga los permisos necesarios.{Colors.RESET}"
        )
        return False
    except OSError as e:
        print(
            f"{Colors.RED}Error al crear el directorio '{path}': {e}" f"{Colors.RESET}"
        )
        return False


def move_file(source_path, dest_path):
    """
    Mueve un archivo de forma segura.

    Args:
        source_path (str): Ruta del archivo de origen
        dest_path (str): Ruta del archivo de destino

    Returns:
        str or None: Ruta de destino si se movió exitosamente, origen si falló
    """
    if not os.path.exists(source_path):
        print(
            f"{Colors.RED}Error: El archivo de origen '{source_path}' no "
            f"existe.{Colors.RESET}"
        )
        return None
    try:
        dest_dir = os.path.dirname(dest_path)
        create_directories(dest_dir)
        shutil.move(source_path, dest_path)
        print(
            f"{Colors.GREEN}Archivo movido exitosamente a: {dest_path}"
            f"{Colors.RESET}"
        )
        return dest_path
    except Exception as e:
        print(f"{Colors.RED}Error al mover el archivo: {e}{Colors.RESET}")
        return source_path


def save_default_path(new_path):
    """
    Guarda la nueva ruta predeterminada usando el sistema de configuración.

    Args:
        new_path (str): Nueva ruta predeterminada a guardar

    Returns:
        bool: True si se guardó exitosamente, False en caso contrario
    """
    try:
        success = config_manager.set_default_path(new_path)
        if success:
            print(
                f"{Colors.GREEN}Nueva ruta predeterminada guardada: {new_path}"
                f"{Colors.RESET}"
            )
            return True
        else:
            print(
                f"{Colors.RED}Error al guardar la nueva ruta predeterminada."
                f"{Colors.RESET}"
            )
            return False
    except Exception as e:
        print(
            f"{Colors.RED}Error al guardar la nueva ruta predeterminada: "
            f"{e}{Colors.RESET}"
        )
        return False


def manage_path_interactive(downloaded_file_path):
    """Gestiona la ruta final de un archivo de forma interactiva."""
    if not downloaded_file_path or not os.path.exists(downloaded_file_path):
        print(
            f"{Colors.YELLOW}Advertencia: No se encontró el archivo "
            f"descargado para mover.{Colors.RESET}"
        )
        return

    while True:
        print(
            "\n" + f"{Colors.BOLD}{Colors.UNDERLINE}{Colors.MAGENTA}Gestión "
            f"de Ruta de Archivo{Colors.RESET}"
        )
        print(
            f"Archivo: "
            f"{Colors.CYAN}{os.path.basename(downloaded_file_path)}"
            f"{Colors.RESET}"
        )
        print(
            f"Ruta actual: "
            f"{Colors.CYAN}{os.path.dirname(downloaded_file_path)}"
            f"{Colors.RESET}\n"
        )
        print(
            f"  {Colors.CYAN}[1]{Colors.RESET} - Usar la ruta "
            f"predeterminada actual (no mover)"
        )
        print(
            f"  {Colors.CYAN}[2]{Colors.RESET} - Mover a otra ruta "
            f"(solo por esta vez)"
        )
        print(
            f"  {Colors.CYAN}[3]{Colors.RESET} - Mover y guardar como nueva "
            f"ruta predeterminada"
        )
        print(f"  {Colors.CYAN}[0]{Colors.RESET} - Finalizar\n")

        choice = get_user_input(f"{Colors.BOLD}Selecciona una opción: {Colors.RESET}")

        if choice == "1" or choice == "0":
            print(
                f"{Colors.GREEN}Archivo guardado en: "
                f"{downloaded_file_path}{Colors.RESET}"
            )
            break
        elif choice == "2":
            new_dir = get_user_input(
                f"{Colors.BOLD}└──> Introduce la nueva ruta de "
                f"directorio: {Colors.RESET}"
            )
            if create_directories(new_dir):
                final_path = os.path.join(
                    new_dir, os.path.basename(downloaded_file_path)
                )
                move_file(downloaded_file_path, final_path)
            break
        elif choice == "3":
            new_dir = get_user_input(
                f"{Colors.BOLD}└──> Introduce la nueva ruta de "
                f"directorio predeterminada: {Colors.RESET}"
            )
            if create_directories(new_dir):
                if save_default_path(new_dir):
                    final_path = os.path.join(
                        new_dir, os.path.basename(downloaded_file_path)
                    )
                    move_file(downloaded_file_path, final_path)
            break
        else:
            print(f"{Colors.RED}Opción no válida.{Colors.RESET}")
