import requests
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

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
        prompt = "fundion DAX más utilizada en Power BI"
        respuesta = obtener_dato_de_prueba(prompt)
        print("\nRespuesta del modelo:")
        print(respuesta)
    except Exception as e:
        print(f"\nOcurrió un error: {e}")