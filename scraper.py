import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept-Language": "es-ES,es;q=0.9"
}


def extraer_datos_alkosto(url):
    """
    Entra a una URL de Alkosto, extrae el título y el precio,
    y devuelve (titulo, precio_final) limpios.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error de conexión: {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extracción del título
        titulo_elem = soup.find('h1')
        titulo = titulo_elem.text.strip() if titulo_elem else "Desconocido"

        # 2. Extracción y limpieza del precio con validación de existencia
        precio_elem = soup.find('span', id='js-original_price')
        if precio_elem and precio_elem.text:
            precio_texto = precio_elem.text.strip()
            # Limpieza en cadena eliminando caracteres no numéricos
            precio_limpio = precio_texto.replace('.', '').replace('$', '').replace('Hoy', '').strip()

            # Caso límite: Si por algún error de selector la cadena queda vacía
            if not precio_limpio.isdigit():
                return titulo, None

            precio_final = int(precio_limpio)
        else:
            precio_final = None

        return titulo, precio_final

    except Exception as e:
        print(f"Ocurrió un error al scrapear: {e}")
        return None, None