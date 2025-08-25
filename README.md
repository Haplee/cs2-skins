# Steam Inventory Price Tracker

Una aplicación web para analizar el valor de tu inventario de skins de CS2, seguir las tendencias de precios y estimar los mejores momentos para comprar o vender.

Esta aplicación está construida con Python y Flask, y está diseñada para ser desplegada fácilmente en plataformas en la nube como Vercel.

## Características

- **Análisis de Inventario de Steam:** Obtiene los artículos de cualquier inventario público de Steam usando un SteamID.
- **Seguimiento de Precios en Tiempo Real:** Obtiene los precios actuales de los artículos desde [Skinport.com](https://skinport.com/).
- **Historial de Precios:** Guarda las consultas de precios en una base de datos para análisis de tendencias a lo largo del tiempo.
- **Análisis de Tendencias:** Compara el precio actual con los promedios históricos para sugerir si un artículo está "Alto", "Bajo" o "Estable" en precio.
- **Interfaz Web Sencilla:** Una interfaz limpia para introducir tu SteamID y ver los resultados.
- **Lista para Desplegar:** Configurada para un despliegue sin problemas en Vercel.

---

## Configuración Local

Para ejecutar esta aplicación en tu máquina local, sigue estos pasos.

### Prerrequisitos

- Python 3.10 o superior
- `pip` para instalar paquetes

### Pasos de Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd <directorio-del-repositorio>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura tus variables de entorno:**
    Para el desarrollo local, puedes establecer las variables de entorno en tu terminal.

    **En Linux/macOS:**
    ```bash
    export STEAM_ID="TU_STEAM_ID_DE_64_BITS"
    export USE_TEST_INVENTORY="false"
    ```

    **En Windows (Command Prompt):**
    ```bash
    set STEAM_ID="TU_STEAM_ID_DE_64_BITS"
    set USE_TEST_INVENTORY="false"
    ```
    *Reemplaza `TU_STEAM_ID_DE_64_BITS` con tu SteamID. Puedes encontrarlo en sitios como [steamidfinder.com](https://steamidfinder.com/).*

5.  **Ejecuta la aplicación:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:8080`.

---

## Despliegue en Vercel

Esta aplicación está lista para ser desplegada en Vercel.

1.  **Crea una cuenta en Vercel:** Si aún no tienes una, regístrate en [vercel.com](https://vercel.com).

2.  **Importa tu Proyecto de Git:**
    - En tu dashboard de Vercel, haz clic en "Add New... -> Project".
    - Importa el repositorio de Git donde se encuentra este proyecto.

3.  **Configura el Proyecto:**
    - Vercel debería detectar automáticamente que es una aplicación Python con Flask.
    - Antes de desplegar, ve a la sección de **"Environment Variables"** (Variables de Entorno) en la configuración de tu proyecto.
    - Añade la siguiente variable de entorno:
        - **Key:** `STEAM_ID`
        - **Value:** `TU_STEAM_ID_DE_64_BITS_AQUI`

4.  **Despliega:**
    - Haz clic en el botón "Deploy".
    - Vercel construirá y desplegará la aplicación. Una vez completado, te proporcionará la URL pública donde tu aplicación está activa.
