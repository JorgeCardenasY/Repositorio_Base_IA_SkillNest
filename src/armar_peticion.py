import os
import requests


def armar_peticion(pregunta_usuario, system_instruction, response_schema=None):
    """Construye la URL y el body usando las variables de entorno.

    Si se proporciona response_schema, la añade como parte del body para
    consultas que requieren un esquema de respuesta específico.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("MODELO")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={api_key}"
        )
    body = {
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
        {"parts": [{"text": pregunta_usuario}]}
            ]
        }
    if response_schema is not None:
            body["generationConfig"] = {
                "responseMimeType": "application/json",
                "responseSchema": response_schema
            }
            return url, body