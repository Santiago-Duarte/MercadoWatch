# MercadoWatch 📈

**MercadoWatch** es una herramienta automatizada de web scraping desarrollada en Python para monitorear, extraer y registrar el historial de precios de productos en plataformas de comercio electrónico, comenzando con Alkosto. 

El objetivo principal es almacenar de forma estructurada las variaciones de costos para identificar ofertas reales y patrones de descuento.

---

## 🛠️ Arquitectura del Proyecto

El sistema está diseñado bajo principios de modularidad y responsabilidad única, dividiendo el código en tres componentes principales:

* **`scraper.py`**: Gestiona la conexión web mediante `requests`, analiza el árbol HTML con `BeautifulSoup` y aplica limpieza de datos en cadenas de texto para aislar valores numéricos puros.
* **`database.py`**: Controla la persistencia de datos local utilizando **SQLite**. Estructura la información en dos tablas relacionales (`productos` e `historial_precios`) con soporte para llaves foráneas y restricciones de unicidad.
* **`main.py`**: El núcleo del programa. Orquesta el flujo de ejecución importando y coordinando los módulos de extracción y almacenamiento.

---

## 🗄️ Modelo de Base de Datos

El diseño relacional mitiga la duplicación de datos (principio DRY) estructurando la información de la siguiente manera:

1.  **Productos**: Almacena los metadatos fijos del artículo.
    * `id` (INTEGER, Llave Primaria)
    * `nombre` (TEXT)
    * `url` (TEXT, Único)
2.  **Historial de Precios**: Registra la evolución del costo en el tiempo.
    * `id` (INTEGER, Llave Primaria)
    * `producto_id` (INTEGER, Llave Foránea vinculada a Productos)
    * `precio` (INTEGER)
    * `fecha` (TIMESTAMP, Captura automática del servidor)

---

## 🚀 Requisitos e Instalación

### Prerrequisitos
* Python 3.x
* IDE compatible (ej. PyCharm)

### Dependencias
Instala las librerías necesarias ejecutando en la terminal:
```bash
pip install requests beautifulsoup4