# main.py
import sys
from notificador import enviar_alerta_telegram
from scraper import extraer_datos_alkosto
from database import inicializar_base_datos, obtener_ultimo_precio, obtener_minimo_historico, registrar_precio_producto
import time
from random import randint

VERDE = "\033[92m"
ROJO = "\033[91m"
RESET = "\033[0m"


def ejecutar_ciclo_monitoreo():
    print("\nIniciando extracción de datos...")
    try:
        with open("urls.txt", "r") as archivo:
            enlaces = [linea.strip() for linea in archivo if linea.strip()]
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo urls.txt")
        return

    for i, enlace in enumerate(enlaces):
        try:
            nombre, precio = extraer_datos_alkosto(enlace)

            if not nombre or not precio:
                print(f"\n❌ Falla en la extracción o estructura HTML cambiada para: {enlace}")
                continue

            print(f"\nScraper exitoso -> Producto: {nombre} | Precio Actual: ${precio}")

            precio_anterior = obtener_ultimo_precio(enlace)
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

            if precio_minimo is not None:
                if precio < precio_minimo:
                    print(f"{VERDE}🔥 [¡NUEVO MÍNIMO HISTÓRICO DETECTADO!]")
                    print(
                        f"¡El precio de {nombre} ha roto su piso de mercado! Nuevo récord: ${precio} (Mínimo anterior: ${precio_minimo}){RESET}")
                    enviar_alerta_telegram(nombre, precio_minimo, precio, enlace)
                elif precio == precio_minimo:
                    print(f"{VERDE}🟢 [PRECIO EN MINIMO HISTÓRICO]")
                    print(f"El precio iguala la mejor oferta registrada: ${precio}{RESET}")
                else:
                    print(f"Nota: El precio actual está por encima del mínimo histórico (${precio_minimo}).")
            else:
                print("ℹ️ Estableciendo el precio actual como el mínimo histórico inicial.")

            registrar_precio_producto(enlace, nombre, precio)

            # Polite anti-blocking delay
            if i < len(enlaces) - 1:
                espera = randint(10, 15)
                print(f"Esperando {espera} segundos para la siguiente petición...")
                time.sleep(espera)

        except Exception as e:
            print(f"❌ Error inesperado procesando el enlace {enlace}: {e}")
            continue


if __name__ == "__main__":
    inicializar_base_datos()

    # Determinar modo de ejecución por argumentos de la terminal
    # Uso estándar (Ideal para Cron): python main.py
    # Uso continuo (Demonio): python main.py --daemon
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        print("🚀 MercadoWatch ejecutándose en modo Demonio (Bucle continuo)...")
        INTERVALO_REVISION = 3600  # 1 hora en segundos
        try:
            while True:
                ejecutar_ciclo_monitoreo()
                print(f"\n💤 Ciclo completado. Hibernando por {INTERVALO_REVISION // 60} minutos...")
                time.sleep(INTERVALO_REVISION)
        except KeyboardInterrupt:
            print("\n🛑 Apagado seguro detectado (KeyboardInterrupt). Cerrando MercadoWatch.")
            sys.exit(0)
    else:
        # Ejecución única (Asilada y limpia)
        ejecutar_ciclo_monitoreo()
        print("\n✨ Ejecución única completada con éxito.")