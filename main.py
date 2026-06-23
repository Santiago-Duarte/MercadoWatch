from scraper import extraer_datos_alkosto
from database import *
import time
from random import randint, choice

# --- CONFIGURACIÓN Y ESTILOS ---
MODO_SIMULACION = True  # Cambiar a False para ejecutar con precios reales de la web

VERDE = "\033[92m"
ROJO = "\033[91m"
RESET = "\033[0m"

if __name__ == "__main__":
    inicializar_base_datos()
    print("\nIniciando extracción de datos...")

    with open("urls.txt", "r") as archivo:
        enlaces = [linea.strip() for linea in archivo if linea.strip()]

    for i, enlace in enumerate(enlaces):
        nombre, precio = extraer_datos_alkosto(enlace)

        # Caso límite: Si el scraper falla, ignoramos el flujo y pasamos al siguiente enlace
        if not nombre or not precio:
            print(f"\n❌ Falla en la extracción para: {enlace}")
            continue

        print(f"\nScraper exitoso -> Producto: {nombre} | Precio Actual: ${precio}")

        # Consultamos el último precio en la BD ANTES de registrar el nuevo
        precio_anterior = obtener_ultimo_precio(enlace)
        # Consultamos el precio mínimo histórico
        precio_minimo = obtener_minimo_historico(enlace)

        if precio_anterior is not None:
            variacion_de_precio = ((precio - precio_anterior) / precio_anterior) * 100

            if variacion_de_precio < 0:
                print(f"{VERDE}🟢 [OFERTA DETECTADA]")
                print(
                    f"El precio de {nombre} ha disminuido: {variacion_de_precio:.2f}% (Antes: ${precio_anterior}){RESET}")
            elif variacion_de_precio > 0:
                print(f"{ROJO}🔴 [ALERTA DE ALZA]")
                print(
                    f"El precio de {nombre} ha aumentado: +{variacion_de_precio:.2f}% (Antes: ${precio_anterior}){RESET}")
            else:
                print("⚪ El precio se mantiene estable sin variaciones.")
        else:
            print("ℹ️ Primer registro de este producto. Monitoreo activado.")

        # 3. EVALUACIÓN DE MÍNIMO HISTÓRICO (Lógica de ofertas reales)
        # Protegemos el flujo contra None si el producto es nuevo
        if precio_minimo is not None:
            if precio < precio_minimo:
                print(f"{VERDE}🔥 [¡NUEVO MÍNIMO HISTÓRICO DETECTADO!]")
                print(
                    f"¡El precio de {nombre} ha roto su piso de mercado! Nuevo récord: ${precio} (Mínimo anterior: ${precio_minimo}){RESET}")
                # Aquí se conectará la función de Telegram más adelante
            elif precio == precio_minimo:
                print(f"{VERDE}🟢 [PRECIO EN MINIMO HISTÓRICO]")
                print(f"El precio iguala la mejor oferta registrada: ${precio}{RESET}")
            else:
                print(f"Nota: El precio actual está por encima del mínimo histórico (${precio_minimo}).")
        else:
            print("ℹ️ Estableciendo el precio actual como el mínimo histórico inicial.")

        # Guardamos el registro de forma persistente en SQLite
        registrar_precio_producto(enlace, nombre, precio)

        # El rate limiting solo se aplica si no es el último elemento
        if i < len(enlaces) - 1:
            espera = randint(10, 15)
            print(f"Esperando {espera} segundos para la siguiente petición...")
            time.sleep(espera)