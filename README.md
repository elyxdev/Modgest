# Modgest 🎮

![Modgest](img/banner.png) *(Si tienes una imagen representativa, colócala en `img/banner.png`)*

**Modgest** es una herramienta de línea de comandos (CLI) y menú interactivo construida en Python, diseñada para simplificar la búsqueda, gestión y descarga de mods de Minecraft utilizando directamente la API de **Modrinth**.

## 🚀 Características Principales

*   **Menú Interactivo:** Navega de forma intuitiva a través de un menú en la terminal (`menu.py`, `ui.py`).
*   **Búsqueda y Descarga Directa:** Busca cualquier mod disponible en Modrinth, selecciona la versión y descárgalo sin salir de la consola (`search_flow.py`, `modrinth_api.py`).
*   **Descargas en Lote (Batch):** Descarga múltiples mods automáticamente leyendo desde un archivo de lista de mods (`batch.py`).
*   **Configuración Persistente:** Guarda tus preferencias de descarga y opciones del programa (`config.py`).
*   **Modo CLI:** Úsalo sin interactividad mediante argumentos pasados por consola (`cli.py`).

## 🛠️ Tecnologías Usadas

*   **Lenguaje:** Python 3.x
*   **Integración de API:** [Modrinth API](https://docs.modrinth.com/) para todo el ecosistema de mods de Minecraft.

## 📦 Instalación y Uso

1.  **Clona este repositorio:**
    ```bash
    git clone https://github.com/elyxdev/Modgest.git
    cd Modgest
    ```

2.  *(Opcional pero recomendado)* **Usa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate     # En Windows
    ```

3.  **Ejecuta el programa:**
    Puedes iniciar el punto de entrada principal para acceder al menú interactivo:
    ```bash
    python modgest.py
    ```

    O utilizar los scripts de compilación incluidos si deseas construir el ejecutable:
    *   En Windows: `build.bat`
    *   En Linux/Mac: `./build.sh`

## 📂 Estructura del Código

El proyecto está modularizado de la siguiente manera:
*   `modgest.py`: Punto de entrada principal que une la configuración, la CLI y el menú.
*   `modrinth_api.py`: Se encarga de todas las peticiones a la API de Modrinth.
*   `search_flow.py`: Controla la lógica de búsqueda, selección y descarga de mods.
*   `batch.py`: Lógica para procesar archivos de lista de mods.
*   `cli.py`: Analizador de argumentos (argparse) para ejecución mediante línea de comandos.
*   `menu.py`: Menú interactivo.
*   `ui.py`: Funciones para entrada/salida y estilización en la consola.
*   `config.py`: Gestor de la configuración persistente del usuario.

## 👨‍💻 Autor y Contribuciones

Desarrollado y mantenido por **Elyx** ([@elyxdev](https://github.com/elyxdev)).

¡Las contribuciones (Issues, Pull Requests) son siempre bienvenidas! Siéntete libre de abrir un issue si encuentras un bug o tienes una sugerencia de mejora.
