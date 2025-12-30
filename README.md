# Termux Ultra Downloader (TUD)

**Herramienta profesional todo-en-uno para Termux, diseñada para descargar, convertir y gestionar contenido multimedia de forma eficiente.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Android%20(Termux)-brightgreen.svg)](https://termux.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> TUD te permite descargar videos y audios, convertir formatos, organizar archivos automáticamente y usar la aplicación tanto desde una interfaz interactiva como por línea de comandos (CLI) para máxima flexibilidad.

---

## 🚀 Características Principales

- **Descarga Multi-Plataforma**: Soporte para descargar contenido de cientos de sitios web gracias a `yt-dlp`.
- **Conversión de Formatos**: Convierte videos a diferentes formatos o extrae el audio en MP3, FLAC, y más, usando `ffmpeg`.
- **Modo Interactivo**: Un menú guiado fácil de usar, perfecto para principiantes.
- **Potente CLI**: Control total a través de la línea de comandos para usuarios avanzados y automatización.
- **Organización Automática**: Los archivos se guardan en una estructura de carpetas lógica por plataforma y tipo de medio.
- **Descarga por Lotes**: Procesa una lista de URLs desde un archivo de texto.
- **Optimizado para Android**: Incluye consejos para evitar que Termux se cierre durante descargas largas.

---

## 🛠️ Instalación y Uso

Sigue estos pasos para poner en marcha Termux Ultra Downloader en tu dispositivo.

### 1. Requisitos Previos
- **Termux**: Instalado desde [F-Droid](https://f-droid.org/packages/com.termux/) (recomendado).
- **Permisos de Almacenamiento**: Ejecuta `termux-setup-storage` en Termux y acepta los permisos.

### 2. Configuración Importante para Termux
Si estás usando esta herramienta en Termux, es posible que necesites configurar los permisos de almacenamiento para poder descargar archivos en las carpetas de tu dispositivo Android:

1. Ejecuta el siguiente comando en Termux:
   ```bash
   termux-setup-storage
   ```

2. Otorga los permisos de almacenamiento cuando se soliciten.

3. Reinicia Termux después de otorgar los permisos.

También puedes usar el script de configuración incluido:
```bash
python scripts/setup_storage.py
```

### 2. Descarga del Proyecto
Para obtener el código fuente, clona este repositorio usando `git`:

```bash
git clone https://github.com/jos669/termux_ultra_downloader.git
cd termux_ultra_downloader
```

### 3. Instalación Automática
El proyecto incluye un script de instalación que configura todo por ti.

```bash
bash scripts/install.sh
```
> **Nota**: El instalador detectará e instalará las dependencias necesarias (`python`, `ffmpeg`, `yt-dlp`) y creará un comando global `tud` para que puedas ejecutar la aplicación desde cualquier directorio.

### 4. Ejecución
Una vez instalado, puedes iniciar la aplicación de dos maneras:

- **Modo Interactivo (Recomendado)**:
  ```bash
  tud
  ```
- **Modo CLI (Avanzado)**:
  Usa `tud --help` para ver todos los comandos y opciones disponibles.

---

## 💡 Ejemplos de Uso (CLI)

```bash
# Descargar un video en la mejor calidad posible a una ruta específica
tud video best "https://youtu.be/dQw4w9WgXcQ" --route /sdcard/Movies/

# Extraer audio en MP3 a 320kbps
tud audio mp3 320 "https://youtu.be/dQw4w9WgXcQ"

# Descargar una playlist completa de videos en 720p
tud playlist video 720 "https://www.youtube.com/playlist?list=PL..."

# Descargar videos masivamente desde un archivo de texto (links.txt)
tud batch video best links.txt
```

---

## 📱 Optimización para Android

- **Evitar que Termux se cierre**: Para descargas largas, ejecuta `termux-wake-lock` en una nueva sesión de Termux antes de iniciar el script.
- **Uso de la batería**: Conecta tu dispositivo a la corriente para procesos largos, ya que la descarga y conversión consumen mucha batería.
- **Log de Errores**: Si algo sale mal, revisa el archivo `downloader.log` dentro de `TermuxDownloader/logs/` para obtener más detalles.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si tienes ideas para mejorar el proyecto, por favor abre un *issue* o envía un *pull request*.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
