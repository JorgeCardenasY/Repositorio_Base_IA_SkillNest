"""Cliente modular de Gemini: envío, reintentos, costo y consulta.

Reúne las cuatro funciones que se prueban en ``test_cliente.py`` de esta misma
carpeta:

- ``enviar_peticion``: hace el POST y **clasifica** los errores.
- ``con_reintento``: repite la llamada cuando el fallo es transitorio.
- ``registrar_costo``: estima y acumula el costo de la sesión.
- ``consultar_modelo``: orquesta las tres anteriores y devuelve el texto.

``requests`` y ``time`` se importan a nivel de módulo a propósito: así las
pruebas pueden reemplazarlos con ``patch("cliente.requests.post")`` y
``patch("cliente.time.sleep")`` sin tocar el resto de la librería.

Existe una copia espejo en el ``cliente.py`` de la raíz (mismos nombres y
comportamiento, con imports prefijados por ``src.``) para poder lanzar la suite
desde cualquiera de las dos carpetas.

Uso:
    python src/cliente.py
"""

import os
import random
import time
from pathlib import Path
from typing import Any, Callable

import requests
from dotenv import load_dotenv

from armar_peticion import armar_peticion
from consulta_y_consumo import extraer_texto

# Ruta absoluta al .env de la raíz: este módulo vive en src/, un nivel abajo.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MODELO = os.getenv("MODELO", "gemini-3.6-flash")
URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODELO}:generateContent?key={os.getenv('GEMINI_API_KEY')}"
)
headers = {"Content-Type": "application/json"}

COSTO_POR_1000_TOKENS = 0.002  # referencial, ajusta según el modelo que uses

costo_total_sesion = 0.0


def enviar_peticion(cuerpo: dict) -> dict:
    """Hace el POST a Gemini y devuelve el JSON; clasifica los fallos.

    - 401/403 -> ``ValueError``: credencial inválida, reintentar no sirve.
    - 429 y 5xx -> ``TimeoutError``: transitorio, conviene reintentar.
    - timeout o ``ConnectionError`` de red -> ``TimeoutError``.
    - otros 4xx (400, 404...) -> deja subir ``requests.HTTPError``.
    """
    try:
        # 60 s: los prompts largos (p. ej. un meme ASCII) tardan ~20-40 s.
        respuesta = requests.post(URL, json=cuerpo, headers=headers, timeout=60)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise TimeoutError("No se pudo contactar al proveedor. Puede ser momentáneo.")

    if respuesta.status_code in (401, 403):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError(
            "El proveedor no pudo procesar la petición. Hay que esperar y reintentar."
        )

    respuesta.raise_for_status()
    return respuesta.json()


def con_reintento(
    funcion: Callable[[], Any],
    intentos: int = 3,
    espera_base: float = 2,
    espera_maxima: float = 30,
) -> Any:
    """Ejecuta ``funcion`` con reintentos y backoff exponencial + jitter.

    Sólo reintenta ``TimeoutError``; cualquier otra excepción sube de inmediato.
    Si se agotan los intentos, propaga la **última** ``TimeoutError`` original.

    La espera es ``min(espera_base * 2 ** (intento - 1), espera_maxima)`` más un
    jitter aleatorio de hasta 10 %: por eso las pruebas no comparan el valor
    exacto, sólo cuántas veces se llamó a ``time.sleep``.
    """
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos:
                raise
            espera = min(espera_base * (2 ** (intento - 1)), espera_maxima)
            espera_con_jitter = espera + random.uniform(0, espera * 0.1)
            print(
                f"Intento {intento} de {intentos} falló. "
                f"Reintentando en {espera_con_jitter:.1f}s..."
            )
            time.sleep(espera_con_jitter)


def registrar_costo(respuesta: dict) -> float:
    """Calcula el costo de una respuesta y lo suma a ``costo_total_sesion``.

    Usa ``usageMetadata.totalTokenCount``; si la respuesta no trae metadata,
    asume 0 tokens en vez de fallar. Devuelve el costo de **esta** operación.
    """
    global costo_total_sesion
    uso = respuesta.get("usageMetadata", {})
    total_tokens = uso.get("totalTokenCount", 0)
    costo_estimado = (total_tokens / 1000) * COSTO_POR_1000_TOKENS
    costo_total_sesion += costo_estimado
    print(
        f"Operación: {total_tokens} tokens, costo estimado: ${costo_estimado:.5f} "
        f"(acumulado: ${costo_total_sesion:.5f})"
    )
    return costo_estimado


def consultar_modelo(pregunta: str, system_instruction: str = "") -> str:
    """Orquesta el flujo: armar -> enviar con reintentos -> costo -> texto.

    Traduce el fallo transitorio agotado a ``RuntimeError`` (el único error que
    ve quien consume el módulo); ``ValueError`` y ``HTTPError`` suben sin cambios.
    """
    _, cuerpo = armar_peticion(pregunta, system_instruction)
    try:
        respuesta = con_reintento(lambda: enviar_peticion(cuerpo))
    except TimeoutError:
        raise RuntimeError(
            "El servicio no respondió tras varios intentos. Intenta más tarde."
        )
    registrar_costo(respuesta)
    return extraer_texto(respuesta)


if __name__ == "__main__":
    print(consultar_modelo("¿Cuál es la capital de Chile?"))
