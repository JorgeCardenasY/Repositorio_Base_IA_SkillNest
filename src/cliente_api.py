import os
import requests
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (por ejemplo GEMINI_API_KEY)
# hacia el entorno del proceso. Sin esta línea, os.getenv("GEMINI_API_KEY")
# devolvería None aunque el .env exista, porque nada lo habría leído todavía.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# El documento de la lección usa "gemini-2.0-flash", pero ese modelo ya fue
# dado de baja por Google (aparece como "Shut down" en su documentación).
# Usamos "gemini-3.8-flash", el modelo Flash vigente más reciente.
URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
)
headers = {"Content-Type": "application/json"}


def enviar_peticion(cuerpo):
    try:
        respuesta = requests.post(URL, json=cuerpo, headers=headers, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise TimeoutError("No se pudo contactar al proveedor. Puede ser momentáneo.")
    if respuesta.status_code in (401, 403):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la petición. Hay que esperar y reintentar.")
    respuesta.raise_for_status()
    return respuesta.json()


if __name__ == "__main__":
    resultado = enviar_peticion({"contents": [{"parts": [{"text": "Hola"}]}]})
    print(resultado)
