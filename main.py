from scraper import extraer_datos_alkosto
from database import inicializar_base_datos, registrar_precio_producto, ver_historial
import time
from random import randint

# --- FLUJO PRINCIPAL DE MERCADOWATCH ---
if __name__ == "__main__":
    # 1. Aseguramos que la base de datos y sus tablas existan antes de operar
    inicializar_base_datos()

    print("\nIniciando extracción de datos...")

    with open("urls.txt", "r") as archivo:
        enlaces = [linea.strip() for linea in archivo if linea.strip()]

    for i, enlace in enumerate(enlaces):
        nombre, precio = extraer_datos_alkosto(enlace)

        if nombre and precio:
            print(f"\nScraper exitoso -> Producto: {nombre} | Precio: {precio}")
            registrar_precio_producto(enlace, nombre, precio)

            # Llamamos a la función de consulta para verificar los datos guardados
            ver_historial(enlace)
        else:
            print(f"\n❌ Falla en la extracción para: {enlace}")

        # El rate limiting solo se aplica si no es el último elemento
        if i < len(enlaces) - 1:
            espera = randint(10, 15)
            print(f"Esperando {espera} segundos para la siguiente petición...")
            time.sleep(espera)