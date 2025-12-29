#!/usr/bin/env python3
import os
import sys

# Agrega el directorio del proyecto al path para poder importar los módulos
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from config import user_settings
from utils.colors import Colors


def main():
    print(f"{Colors.YELLOW}--- INICIANDO CORRECCIÓN DE RUTA DE DESCARGA ---{Colors.RESET}")

    # 1. Define la nueva ruta de descarga segura dentro del home de Termux
    home_dir = os.path.expanduser('~')
    new_safe_path = os.path.join(home_dir, 'Termux_Downloads')

    print(f"Ruta de descarga anterior: {user_settings.get_default_path()}")
    print(f"Nueva ruta de descarga segura a establecer: {new_safe_path}")

    # 2. Crea el directorio si no existe
    if not os.path.exists(new_safe_path):
        print(f"Creando directorio: {new_safe_path}")
        os.makedirs(new_safe_path)

    # 3. Llama a la función existente para guardar la nueva configuración
    try:
        user_settings.set_default_path(new_safe_path)
        print(f"\n{Colors.GREEN}--- CORRECCIÓN APLICADA EXITOSAMENTE ---{Colors.RESET}")
        print("La ruta de descarga predeterminada ahora es segura y se encuentra dentro del directorio de Termux.")
        print("Por favor, ejecuta el programa principal de nuevo ('python main.py') y verifica que la descarga funcione.")
    except Exception as e:
        print(f"\n{Colors.RED}--- FALLO LA CORRECCIÓN AUTOMÁTICA ---{Colors.RESET}")
        print(f"Ocurrió un error al intentar guardar la nueva configuración: {e}")
        print("Por favor, intenta cambiar la ruta manualmente desde el menú de la aplicación (Opción 5).")



if __name__ == "__main__":
    main()
