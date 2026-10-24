import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def armar_peticion_imagen(pregunta, imagen_base64=None, mime_type="image/png"):
    """Construye la URL y el body usando las variables de entorno.

    Si se proporciona imagen_base64, la añade como parte inlineData para
    consultas multimodales (por ejemplo, reconocimiento de imágenes).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("MODELO")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={api_key}"
    )

    parts = [{"text": pregunta}]
    if imagen_base64:
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": imagen_base64,
            }
        })

    body = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }
    return url, body
