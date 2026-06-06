from scraper import extraer_datos_alkosto
from database import inicializar_base_datos, registrar_precio_producto

# --- FLUJO PRINCIPAL DE MERCADOWATCH ---
if __name__ == "__main__":
    # 1. Aseguramos que la base de datos y sus tablas existan antes de operar
    inicializar_base_datos()

    # URL del producto en Alkosto
    enlace = "https://www.alkosto.com/audifonos-apple-airpods-pro-3-estuche-magsafe-usb-c-blanco/p/195950543612"

    print("\nIniciando extracción de datos...")
    # 2. Corremos el scraper para obtener la información fresca de la web
    nombre, precio = extraer_datos_alkosto(enlace)

    # 3. Verificamos que el scraper haya tenido éxito antes de intentar guardar
    if nombre and precio:
        print(f"Scraper exitoso -> Producto: {nombre} | Precio: {precio}")

        # 4. Guardamos el registro de forma persistente en SQLite
        registrar_precio_producto(enlace, nombre, precio)
    else:
        print("❌ No se pudieron obtener los datos del producto. Revisa el scraper.")