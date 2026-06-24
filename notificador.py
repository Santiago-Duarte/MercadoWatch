# notificador.py
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID_TELEGRAM = os.getenv("CHAT_ID_TELEGRAM")

def enviar_alerta_telegram(producto, precio_anterior, precio_nuevo, url):
    """Envia un mensaje formateado a Telegram notificando un nuevo minimo historico."""
    if not TOKEN_TELEGRAM or not CHAT_ID_TELEGRAM:
        print("❌ Error: Credenciales de Telegram no configuradas en el entorno.")
        return

    descuento_absoluto = precio_anterior - precio_nuevo
    porcentaje = ((precio_anterior - precio_nuevo) / precio_anterior) * 100

    mensaje = (
        f"🔥 *¡NUEVO MÍNIMO HISTÓRICO!*\n\n"
        f"📦 *Producto:* {producto}\n"
        f"📉 *Descuento:* -{porcentaje:.2f}% (-${descuento_absoluto:,})\n"
        f"💰 *Precio Anterior:* ${precio_anterior:,}\n"
        f"🚀 *Precio Nuevo:* ${precio_nuevo:,}\n\n"
        f"🔗 [Ver producto en Alkosto]({url})"
    )

    url_api = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID_TELEGRAM,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        respuesta = requests.post(url_api, json=payload, timeout=10)
        if respuesta.status_code == 200:
            print("✈️ Notificación de Telegram enviada con éxito.")
        elif respuesta.status_code == 401:
            print("❌ Error 401: El token actual de Telegram no es válido. Genere uno nuevo con /token en @BotFather.")
        else:
            print(f"⚠️ Telegram respondió con código {respuesta.status_code}: {respuesta.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de red al conectar con Telegram: {e}")

if __name__ == "__main__":
    enviar_alerta_telegram("Producto de Prueba", 1500000, 1200000, "https://www.alkosto.com")