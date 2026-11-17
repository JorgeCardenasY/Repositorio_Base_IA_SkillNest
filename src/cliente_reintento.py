"""
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


import time
import random
from typing import Callable, Any


def con_reintento(
    funcion: Callable[[], Any],
    intentos: int = 3,
    espera_base: float = 2,
    espera_maxima: float = 30,
) -> Any:
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos:
                raise
            espera = min(espera_base * (2 ** (intento - 1)), espera_maxima)
            espera_con_jitter = espera + random.uniform(0, espera * 0.1)
            print(f"Intento {intento} de {intentos} falló. Reintentando en {espera_con_jitter:.1f}s...")
            time.sleep(espera_con_jitter)


COSTO_POR_1000_TOKENS = 0.002  # referencial, ajusta según el modelo que uses
costo_total_sesion = 0.0


def registrar_costo(respuesta: dict) -> float:
    global costo_total_sesion
    uso = respuesta.get("usageMetadata", {})
    total_tokens = uso.get("totalTokenCount", 0)
    costo_estimado = (total_tokens / 1000) * COSTO_POR_1000_TOKENS
    costo_total_sesion += costo_estimado
    print(f"Operación: {total_tokens} tokens, costo estimado: ${costo_estimado:.5f} (acumulado: ${costo_total_sesion:.5f})")
    return costo_estimado


def consultar_modelo(pregunta: str, system_instruction: str = "") -> str:
    url, body = armar_peticion(pregunta, system_instruction)
    try:
        respuesta = con_reintento(lambda: enviar_peticion(url, body))
    except TimeoutError:
        raise RuntimeError("El servicio no respondió tras varios intentos. Intenta más tarde.")
    registrar_costo(respuesta)
    return extraer_texto(respuesta)


if __name__ == "__main__":
    resultado = consultar_modelo("¿Capital de Chile?")
    print(resultado)
