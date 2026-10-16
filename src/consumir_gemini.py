import os
import requests
from dotenv import load_dotenv

load_dotenv()

def obtener_dato_de_prueba(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("modelo")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={api_key}"
    )

    body = {
        "contents": [
            {
                "parts": [
                    {"text": pregunta}
                ]
            }
        ]
    }

    respuesta = requests.post(url, json=body)
    respuesta.raise_for_status()  # lanza error claro si falla
    datos = respuesta.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    respuesta = obtener_dato_de_prueba("clima de Arica, Chile mañana")
    print(respuesta)
