#!/bin/bash

# ---[ COLORES Y ESTILOS ]----------------
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_RED='\033[31m'
C_GREEN='\033[32m'
C_YELLOW='\033[33m'
C_CYAN='\033[36m'
C_WHITE='\033[37m'

# ---[ CONFIGURACIÓN ]--------------------
# Detectar el directorio del script para encontrar main.py
# Esto permite ejecutar el instalador desde cualquier lugar.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_DIR=$(cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd)
MAIN_PY_PATH="$PROJECT_DIR/main.py"
CMD_NAME="tud"
INSTALL_PATH="$PREFIX/bin/$CMD_NAME"

# ---[ FUNCIONES AUXILIARES ]-------------
print_status() {
    echo -e "${C_CYAN}[*] $1${C_RESET}"
}

print_success() {
    echo -e "${C_GREEN}[+] $1${C_RESET}"
}

print_error() {
    echo -e "${C_RED}[-] $1${C_RESET}"
}

print_warning() {
    echo -e "${C_YELLOW}[!] $1${C_RESET}"
}

check_termux() {
    if [ -z "$PREFIX" ] || ! echo "$PREFIX" | grep -q "com.termux"; then
        print_error "Este script está diseñado para ejecutarse exclusivamente en Termux."
        exit 1
    fi
    print_success "Entorno Termux detectado."
}

# ---[ FUNCIONES PRINCIPALES ]------------

check_installation_status() {
    print_status "Verificando el estado de la instalación..."
    local all_ok=true

    # 1. Dependencias de Termux
    print_status "Verificando paquetes de Termux (python, ffmpeg)..."
    for pkg in python ffmpeg; do
        if command -v "$pkg" > /dev/null; then
            print_success "$pkg está instalado."
        else
            print_error "$pkg NO está instalado."
            all_ok=false
        fi
    done

    # 2. Dependencias de Python
    print_status "Verificando paquetes de Python (yt-dlp)..."
    if python -c "import yt_dlp" > /dev/null 2>&1; then
        print_success "yt-dlp está instalado."
    else
        print_error "yt-dlp NO está instalado."
        all_ok=false
    fi

    # 3. Comando global
    print_status "Verificando comando global '$CMD_NAME'..."
    if [ -f "$INSTALL_PATH" ]; then
        print_success "El comando '$CMD_NAME' está instalado en $INSTALL_PATH."
    else
        print_error "El comando '$CMD_NAME' NO está instalado."
        all_ok=false
    fi
    
    # 4. Verificación de ruta del proyecto en el comando
    if [ -f "$INSTALL_PATH" ]; then
        if grep -q "PROJECT_DIR=\"$PROJECT_DIR\"" "$INSTALL_PATH"; then
            print_success "La ruta del proyecto en el comando '$CMD_NAME' es correcta."
        else
            print_error "La ruta del proyecto en el comando '$CMD_NAME' es incorrecta o desactualizada."
            all_ok=false
        fi
    fi


    if [ "$all_ok" = true ]; then
        print_success "\n¡Todo parece estar correctamente instalado y listo para usar!"
    else
        print_warning "\nSe encontraron problemas. Se recomienda ejecutar la opción de instalación."
    fi
}

install_dependencies() {
    print_status "Instalando/actualizando dependencias..."
    
    # Paquetes de Termux
    pkg install python ffmpeg -y || { print_error "Falló la instalación de paquetes de Termux."; return 1; }

    # Paquetes de Python
    pip install -r "$PROJECT_DIR/requirements.txt" || { print_error "Falló la instalación de requerimientos de Python."; return 1; }
    
    print_success "Dependencias instaladas correctamente."
    return 0
}

install_global_command() {
    print_status "Instalando el comando global '$CMD_NAME' en $INSTALL_PATH..."

    # Crear el script que actuará como comando global
    # Usamos '#!/data/data/com.termux/files/usr/bin/bash' para máxima compatibilidad en Termux
    cat > "$INSTALL_PATH" << EOF
#!/data/data/com.termux/files/usr/bin/bash

# Este script ejecuta Termux Ultra Downloader (tud)
# Se cambia al directorio del proyecto y luego ejecuta main.py con todos los argumentos.

# Directorio absoluto donde se encuentra main.py
PROJECT_DIR="$PROJECT_DIR"
MAIN_PY_PATH="$MAIN_PY_PATH"

# Verificar si el directorio del proyecto existe
if [ ! -d "\$PROJECT_DIR" ]; then
    echo -e "\033[31mError: El directorio del proyecto '\
$PROJECT_DIR' no se encuentra.\033[0m"
    echo -e "\033[33mPor favor, reinstala la herramienta o verifica la ruta.\033[0m"
    exit 1
fi

# Ejecutar el script de Python principal, pasando todos los argumentos del comando
cd "\$PROJECT_DIR" && python "\$MAIN_PY_PATH" "\$@"

EOF

    # Dar permisos de ejecución
    chmod +x "$INSTALL_PATH"

    if [ -f "$INSTALL_PATH" ]; then
        print_success "Comando '$CMD_NAME' instalado exitosamente."
        print_warning "Puede que necesites reiniciar tu sesión de Termux para usar el comando."
        return 0
    else
        print_error "La instalación del comando falló."
        return 1
    fi
}

run_without_install() {
    print_status "Ejecutando el script sin instalar..."
    print_warning "Asegúrate de que todas las dependencias estén instaladas."
    
    # Cambiar al directorio del proyecto y ejecutar main.py
    (cd "$PROJECT_DIR" && python "$MAIN_PY_PATH")
    
    echo -e "\n${C_YELLOW}Presiona Enter para volver al menú principal del instalador...${C_RESET}"
    read -r -s -n 1
}

uninstall_command() {
    print_status "Desinstalando el comando global '$CMD_NAME'..."

    if [ -f "$INSTALL_PATH" ]; then
        rm -f "$INSTALL_PATH"
        if [ $? -eq 0 ]; then
            print_success "Comando '$CMD_NAME' desinstalado correctamente."
        else
            print_error "No se pudo eliminar el archivo del comando."
        fi
    else
        print_warning "El comando '$CMD_NAME' no estaba instalado."
    fi
}

# ---[ MENÚ PRINCIPAL DEL INSTALADOR ]----

main_menu() {
    while true; do
        clear
        echo -e "${C_BOLD}${C_WHITE}--- Instalador de Termux Ultra Downloader ---${C_RESET}"
        echo -e "Directorio del proyecto: ${C_CYAN}$PROJECT_DIR${C_RESET}"
        echo -e "Ruta de instalación: ${C_CYAN}$INSTALL_PATH${C_RESET}\n"
        
        echo -e "${C_YELLOW}Elige una opción:${C_RESET}"
        echo "  [1] Instalar (Dependencias + Comando Global 'tud')"
        echo "  [2] Ejecutar el script (sin instalar como comando global)"
        echo "  [3] Desinstalar (Eliminar el comando 'tud')"
        echo "  [4] Verificar estado de la instalación"
        echo "  [0] Salir"
        echo ""
        read -p "Opción: " choice

        case $choice in
            1)
                check_termux
                print_status "Solicitando permiso de almacenamiento..."
                termux-setup-storage
                install_dependencies && install_global_command
                echo -e "\n${C_YELLOW}Presiona Enter para continuar...${C_RESET}"
                read -r -s -n 1
                ;;
            2)
                check_termux
                run_without_install
                ;;
            3)
                check_termux
                uninstall_command
                echo -e "\n${C_YELLOW}Presiona Enter para continuar...${C_RESET}"
                read -r -s -n 1
                ;;
            4)
                check_termux
                check_installation_status
                echo -e "\n${C_YELLOW}Presiona Enter para continuar...${C_RESET}"
                read -r -s -n 1
                ;;
            0)
                echo "Saliendo."
                exit 0
                ;;
            *)
                print_error "Opción no válida."
                sleep 1
                ;;
        esac
    done
}

# ---[ EJECUCIÓN ]-----------------------
main_menu
