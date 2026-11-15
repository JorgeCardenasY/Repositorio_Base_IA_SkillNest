import requests
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Gemini recibe la API key en la cabecera x-goog-api-key, no como "Bearer".
headers = {
    "x-goog-api-key": os.getenv("GEMINI_API_KEY"),
    "Content-Type": "application/json",
}


def enviar_peticion(url, body):
    """Realiza la petición HTTP y devuelve el JSON."""

    # Se agregan 3 formas de manejar errores: 1) credenciales inválidas,
    # 2) límite de peticiones alcanzado, 3) error del servidor.

    try:
        # 60 s: los prompts largos (p. ej. generar un meme ASCII) tardan ~20-40 s.
        respuesta = requests.post(url, json=body, headers=headers, timeout=60)
    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ):
        raise TimeoutError("No se pudo contactar al proveedor. Puede ser momentáneo.")

    if respuesta.status_code == 429:
        segundos = respuesta.headers.get("Retry-After")
        mensaje = (
            f"Límite excedido. Reintentar en {segundos}s."
            if segundos
            else "Límite excedido."
        )
        raise TimeoutError(mensaje)
    if respuesta.status_code in (401, 403):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la petición. Hay que esperar y reintentar.")

    respuesta.raise_for_status()
    return respuesta.json()

    # Referencia histórica: versión anterior del manejo de errores (no se ejecuta).
    """
        #Se incorpora un timeout de 10 segundos para evitar que la petición quede colgada indefinidamente.
        if respuesta.status_code in (401, 403):
            raise ValueError("Credenciales inválidas. Verifica tu API key.")
        if respuesta.status_code == 429:
            raise ValueError("Se ha alcanzado el límite de peticiones. Intenta más tarde.")
        if respuesta.status_code >= 500:
            raise ValueError(" >.< Error del servidor. Intenta más tarde.")
        respuesta.raise_for_status()  # Lanza error claro si falla la petición HTTP
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error en la petición al servicio: {e}")
    """


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
    from armar_peticion import armar_peticion
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
        prompt = "imprime un meme en codigo ascii"
        respuesta = obtener_dato_de_prueba(prompt)
        print("\nRespuesta del modelo:")
        print(respuesta)
    except Exception as e:
        print(f"\nOcurrió un error: {e}")