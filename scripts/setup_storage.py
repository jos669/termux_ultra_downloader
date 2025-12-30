#!/usr/bin/env python3
"""
Script para ayudar a configurar los permisos de almacenamiento en Termux.
"""

import os
import sys
import subprocess


def check_termux_storage():
    """Verifica si los permisos de almacenamiento están configurados en Termux."""
    storage_path = os.path.expanduser("~/storage/downloads")
    
    if os.path.exists(storage_path):
        if os.access(storage_path, os.W_OK):
            print("✅ Los permisos de almacenamiento están configurados correctamente.")
            print(f"📁 Ruta de descargas accesible: {storage_path}")
            return True
        else:
            print("⚠️  Los permisos de almacenamiento están configurados pero no se puede escribir.")
            print(f"   Verifica los permisos para: {storage_path}")
            return False
    else:
        print("❌ Los permisos de almacenamiento no están configurados.")
        print("   La ruta ~/storage/downloads no existe.")
        return False


def setup_termux_storage():
    """Ejecuta el comando para configurar los permisos de almacenamiento en Termux."""
    print("🔧 Configurando permisos de almacenamiento de Termux...")
    print("   Se abrirá un diálogo para otorgar permisos de almacenamiento.")
    print("   Por favor, acepta los permisos cuando se soliciten.")
    print()
    
    try:
        # Ejecutar termux-setup-storage
        result = subprocess.run(["termux-setup-storage"], check=True)
        
        if result.returncode == 0:
            print("✅ Configuración de almacenamiento completada exitosamente.")
            print("📁 Ahora puedes acceder a los directorios de almacenamiento externo.")
            return True
        else:
            print("❌ Error al configurar los permisos de almacenamiento.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar termux-setup-storage: {e}")
        return False
    except FileNotFoundError:
        print("❌ El comando 'termux-setup-storage' no se encontró.")
        print("   Asegúrate de estar ejecutando este script dentro de Termux.")
        return False


def main():
    """Función principal del script."""
    print("🔧 Asistente de Configuración de Almacenamiento para Termux")
    print("=" * 55)
    
    if not check_termux_storage():
        print()
        response = input("¿Deseas configurar los permisos de almacenamiento ahora? (s/n): ")
        
        if response.lower() in ['s', 'si', 'y', 'yes']:
            if setup_termux_storage():
                print()
                print("🎉 ¡Listo! Ahora puedes usar las rutas de almacenamiento externo.")
                print("   Recuerda reiniciar Termux si es necesario.")
            else:
                print()
                print("❌ No se pudo configurar el almacenamiento. Inténtalo manualmente:")
                print("   1. Abre Termux")
                print("   2. Ejecuta: termux-setup-storage")
                print("   3. Otorga los permisos solicitados")
        else:
            print("⚠️  Configuración cancelada. El programa usará rutas locales.")
    else:
        print("✅ El sistema ya está configurado correctamente.")


if __name__ == "__main__":
    main()