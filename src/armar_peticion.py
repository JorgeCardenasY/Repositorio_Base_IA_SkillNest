import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def armar_peticion(pregunta_usuario, system_instruction="", response_schema=None):
    """Construye la URL y el body usando las variables de entorno.

    Si se proporciona system_instruction, lo envía como systemInstruction.
    Si se proporciona response_schema, fuerza una respuesta JSON con ese esquema.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("MODELO")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={api_key}"
    )

    body = {
        "contents": [
            {"parts": [{"text": pregunta_usuario}]}
        ]
    }

    if system_instruction:
        body["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema,
        }

    return url, body
