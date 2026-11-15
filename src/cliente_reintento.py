"""Consulta a Gemini con reintentos ante fallos transitorios.

Envuelve el cliente real del proyecto (`consulta_y_consumo.enviar_peticion`)
con una política de reintentos y backoff exponencial:

- Reintenta solo errores transitorios: `TimeoutError`, que es lo que ya
traduce `consulta_y_consumo.enviar_peticion` para timeout de red,
ConnectionError, HTTP 429 y HTTP 5xx.
- Aborta de inmediato ante errores definitivos: `ValueError` (HTTP 401/403,
credencial inválida) y `requests.HTTPError` (HTTP 400/404, petición mal
formada o modelo inexistente), porque reintentarlos solo gasta cuota.

Uso:
    python src/cliente_reintento.py
"""

import os
import random
import time
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from requests.exceptions import HTTPError

from armar_peticion import armar_peticion
from consulta_y_consumo import calcular_costo, enviar_peticion, extraer_texto
from parsear_respuesta import parsear_respuesta_json

# Ruta absoluta al .env de la raíz: funciona desde cualquier directorio de trabajo.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# --- Política de reintentos -------------------------------------------------
INTENTOS = 3
ESPERA_BASE = 2.0
ESPERA_MAXIMA = 30.0


# Precios de referencia: mismos valores aproximados que usa consulta_y_consumo.py.
PRECIO_ENTRADA = 0.00000075
PRECIO_SALIDA = 0.000000375

# --- La consulta ------------------------------------------------------------
SYSTEM_INSTRUCTION = """
Eres un asistente técnico. Responde SIEMPRE en formato JSON válido,
sin texto antes ni después, usando exactamente estas claves:
- "categoria": tema principal de la pregunta (texto corto).
- "confianza": qué tan seguro estás, número entero de 0 a 100.
- "explicacion": tu respuesta, en un máximo de 3 oraciones.
No agregues bloques de código ni comentarios fuera del JSON.
"""

PREGUNTA = "en cuanto ha subido el precio del petróleo en Chile en los últimos 3 meses y por qué"

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "categoria": {"type": "STRING"},
        "confianza": {"type": "INTEGER"},
        "explicacion": {"type": "STRING"},
    },
    "required": ["categoria", "confianza", "explicacion"],
}

CLAVES_ESPERADAS = ["categoria", "confianza", "explicacion"]


def validar_configuracion() -> None:
    """Comprueba que el .env trae lo mínimo para poder consultar.

    Raises:
        RuntimeError: si falta GEMINI_API_KEY o MODELO en el .env.
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "Falta GEMINI_API_KEY en el .env: copia .env.example y complétalo."
        )
    if not os.getenv("MODELO"):
        raise RuntimeError(
            "Falta MODELO en el .env (es la variable que usa armar_peticion.py)."
        )


def con_reintento(
    funcion: Callable[[], Any],
    intentos: int = INTENTOS,
    espera_base: float = ESPERA_BASE,
    espera_maxima: float = ESPERA_MAXIMA,
) -> tuple[Any, int]:
    """Ejecuta `funcion` hasta `intentos` veces ante fallos transitorios.

    Solo reintenta `TimeoutError`. Cualquier otra excepción (credencial
    inválida, petición mal formada, respuesta sin texto) se propaga de
    inmediato para no gastar cuota.

    Args:
        funcion: Función sin argumentos que hace la llamada.
        intentos: Número máximo de intentos; debe ser 1 o más.
        espera_base: Segundos de espera después del primer fallo.
        espera_maxima: Tope de la espera entre reintentos.

    Returns:
        tuple: (resultado de `funcion`, número de intento en que se logró).

    Raises:
        ValueError: si `intentos` es menor que 1.
        TimeoutError: si se agotan todos los intentos.
    """
    if intentos < 1:
        raise ValueError("'intentos' debe ser 1 o más")

    for intento in range(1, intentos + 1):
        try:
            return funcion(), intento
        except TimeoutError as error:
            if intento == intentos:
                raise TimeoutError(
                    f"Falló tras {intentos} intentos: {error}"
                ) from error
            espera = min(espera_base * 2 ** (intento - 1), espera_maxima)
            espera += random.uniform(0, espera * 0.1)  # jitter: reintentos no sincronizados
            print(
                f"Intento {intento} de {intentos} falló ({error}). "
                f"Reintentando en {espera:.1f}s..."
            )
            time.sleep(espera)


def hacer_consulta(pregunta: str, intentos: int = INTENTOS) -> dict:
    """Arma, envía (con reintentos), extrae y parsea una consulta.

    Args:
        pregunta: Texto de la pregunta del usuario.
        intentos: Número máximo de intentos de la política de reintentos.

    Returns:
        dict: claves `intento`, `texto` (crudo del modelo), `datos`
        (diccionario parseado) y `costo` (USD estimado).

    Raises:
        ValueError: credencial inválida (HTTP 401/403) o respuesta que no
            respeta el esquema JSON.
        RuntimeError: petición rechazada (HTTP 400/404).
        TimeoutError: sin respuesta tras agotar los intentos.
    """
    url, body = armar_peticion(pregunta, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)

    try:
        respuesta, intento = con_reintento(
            lambda: enviar_peticion(url, body), intentos=intentos
        )
    except HTTPError as error:
        codigo = error.response.status_code if error.response is not None else "?"
        raise RuntimeError(
            f"El proveedor rechazó la petición (HTTP {codigo}). "
            "Revisa la variable MODELO del .env."
        ) from error

    texto = extraer_texto(respuesta)
    return {
        "intento": intento,
        "texto": texto,
        "datos": parsear_respuesta_json(texto, CLAVES_ESPERADAS),
        "costo": calcular_costo(respuesta, PRECIO_ENTRADA, PRECIO_SALIDA),
    }


def main() -> int:
    """Ejecuta una consulta con reintentos y muestra el resultado.

    Returns:
        int: 0 si la consulta se completó; 1 si hubo un error controlado.
    """
    try:
        validar_configuracion()
        resultado = hacer_consulta(PREGUNTA)
    except (ValueError, RuntimeError) as error:
        print(f"\nNo se pudo completar la consulta: {error}")
        return 1
    except TimeoutError as error:
        print(f"\nLa API no respondió tras varios intentos: {error}")
        return 1

    print(f"Respuesta lograda en el intento {resultado['intento']} de {INTENTOS}.")
    print("Texto tal cual lo escribió el modelo:")
    print(resultado["texto"])
    print("\nRespuesta ordenada en campos:")
    for nombre, valor in resultado["datos"].items():
        print(f"  {nombre}: {valor}")
    print(f"\nCosto estimado de la operación: ${resultado['costo']:.6f} USD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

