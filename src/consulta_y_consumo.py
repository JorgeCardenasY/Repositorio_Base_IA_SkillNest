import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def armar_peticion(pregunta, imagen_base64=None, mime_type="image/png"):
    """Construye la URL y el body usando las variables de entorno.

    Si se proporciona imagen_base64, la añade como parte inlineData para
    consultas multimodales (por ejemplo, reconocimiento de imágenes).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = os.getenv("modelo")

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

def enviar_peticion(url, body):
    """Realiza la petición HTTP y devuelve el JSON."""
    try:
        respuesta = requests.post(url, json=body)
        respuesta.raise_for_status()  # Lanza error claro si falla la petición HTTP
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error en la petición al servicio: {e}")

def extraer_texto(datos):
    """Extrae el texto generado del JSON de respuesta."""
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")

def calcular_costo(datos, precio_entrada, precio_salida):
    """Calcula el costo basado en los tokens consumidos."""
    try:
        uso = datos["usageMetadata"]

        tokens_entrada = uso["promptTokenCount"]
        tokens_salida = uso["candidatesTokenCount"]
        tokens_razonamiento = uso.get("thoughtsTokenCount", 0)

        costo = (
            tokens_entrada * precio_entrada
            + (tokens_salida + tokens_razonamiento) * precio_salida
        )

        return costo
    except KeyError:
        # En caso de que no venga metadata de uso, evitamos que el programa falle
        return 0.0

def obtener_dato_de_prueba(pregunta):
    """Función principal que orquesta el flujo."""
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    
    # precios aproximados: Se pueden ajustar según la documentación oficial
    costo = calcular_costo(datos, 0.00000075, 0.000000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    
    return extraer_texto(datos)

if __name__ == "__main__":
    try:
        # Prompt.
        # 
        prompt = "fundion DAX más utilizada en Power BI"
        respuesta = obtener_dato_de_prueba(prompt)
        print("\nRespuesta del modelo:")
        print(respuesta)
    except Exception as e:
        print(f"\nOcurrió un error: {e}")