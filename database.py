import sqlite3

DB_NAME = "mercadowatch.db"


def inicializar_base_datos():
    """Crea el archivo de la base de datos y las tablas si no existen."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Activar el soporte para llaves foráneas (relaciones entre tablas)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL
        )
    ''')

    # 2. Crear tabla de historial de precios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            precio INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')

    conexion.commit()
    conexion.close()
    print("¡Base de datos e intérprete de comandos listos!")


def registrar_precio_producto(url, nombre, precio):
    """Inserta el producto si no existe y registra su precio en el historial."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        # 1. Insertar el producto (si ya existe la URL, lo ignora)
        cursor.execute('''
            INSERT OR IGNORE INTO productos (nombre, url) 
            VALUES (?, ?)
        ''', (nombre, url))

        # 2. Buscar el ID del producto basado en la URL
        cursor.execute('SELECT id FROM productos WHERE url = ?', (url,))
        producto_id = cursor.fetchone()[0]

        # 3. Insertar el precio en el historial histórico
        cursor.execute('''
            INSERT INTO historial_precios (producto_id, precio) 
            VALUES (?, ?)
        ''', (producto_id, precio))

        conexion.commit()
        print(f"✓ Guardado en BD -> {nombre}: ${precio}")

    except Exception as e:
        print(f"Error en la base de datos: {e}")
        conexion.rollback()
    finally:
        conexion.close()