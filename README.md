# Termux Ultra Downloader

Herramienta profesional todo-en-uno para Termux, capaz de descargar video y audio, convertir formatos, organizar archivos y ejecutarse tanto por una interfaz interactiva como por línea de comandos (CLI).

## 1. Requisitos Previos
- Tener Termux instalado desde F-Droid (recomendado).
- Acceso al almacenamiento compartido. Ejecuta `termux-setup-storage` en la consola de Termux y acepta el permiso.

## 2. Instrucciones de Instalación

**¡Importante!** Ejecuta el script `install.sh` para la configuración automática:

```bash
cd termux_ultra_downloader  # Navega al directorio raíz del proyecto
bash scripts/install.sh
```

El instalador te guiará para:
- Detectar e instalar dependencias (python, ffmpeg, yt-dlp).
- Solicitar permisos de almacenamiento.
- Crear el comando global `tud` para ejecutar la aplicación fácilmente desde cualquier lugar.

## 3. Ejecución

### Modo Interactivo (Recomendado para principiantes)
Para iniciar el menú guiado, simplemente ejecuta:
```bash
tud
```
o si no instalaste el comando global:
```bash
python main.py
```

### Modo CLI (Línea de Comandos)
Para uso avanzado y automatización.
Una vez instalado el comando global `tud`, la sintaxis es:
`tud [comando] [argumentos...]`

**Usa `tud --help` o `tud [comando] --help` para ver todas las opciones.**

**Ejemplos Reales:**
```bash
# Verificar e instalar dependencias si es necesario
tud setup

# Mostrar la configuración actual
tud config show

# Cambiar la ruta de descarga predeterminada
tud config set DOWNLOADS_BASE_DIR /sdcard/MisDescargasTUD/

# Descargar un video en calidad 1080p
tud video 1080p https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Descargar un video en la mejor calidad posible a una ruta específica
tud video best https://... --route /sdcard/Movies/

# Extraer audio en MP3 a 320k y guardar la ruta como nueva predeterminada
tud audio mp3 320 https://... --route /sdcard/Music/MyBand/ --save-route

# Descargar una playlist completa de videos en 720p
tud playlist video 720 https://...

# Extraer el audio de una playlist en formato FLAC, mostrando más detalles
tud playlist audio flac best https://... --verbose

# Descargar videos masivamente desde un archivo de texto (links.txt)
tud batch video best links.txt

# Monitorear un archivo 'nuevas_urls.txt' y descargar automáticamente las URLs añadidas
tud watch nuevas_urls.txt

# Mostrar el comando yt-dlp que se ejecutaría para una descarga de audio sin ejecutarla
tud audio mp3 320 https://... --dry-run
```

## 4. Organización de Archivos
- Todos los archivos se guardan en la carpeta `TermuxDownloader` en tu almacenamiento compartido (visible para otras apps). Esta ruta se puede configurar.
- Dentro, se crean carpetas por plataforma (YouTube, TikTok, etc.).
- Dentro de cada plataforma, hay subcarpetas `video` y `audio`.
- Los archivos se nombran con `FECHA_Titulo.extension` para fácil organización.

## 5. Tips de Optimización para Android
- **Evitar que Termux se cierre**: Para descargas largas, usa el comando `termux-wake-lock` en una nueva sesión de Termux antes de iniciar el script. Para detenerlo, usa `termux-wake-unlock`.
- **Uso de la batería**: Las descargas y conversiones consumen mucha batería. Conecta el dispositivo a la corriente para procesos largos.
- **Almacenamiento**: Verifica tener suficiente espacio. Los archivos se guardan en el almacenamiento compartido, facilitando su gestión.
- **Errores de Red**: Si una descarga falla por problemas de red, el script intentará continuarla en la siguiente ejecución gracias a la opción `--continue` de `yt-dlp`.
- **Log de Errores**: Si algo sale mal, revisa el archivo `downloader.log` dentro de la carpeta `TermuxDownloader/logs/` para obtener pistas sobre el problema.
