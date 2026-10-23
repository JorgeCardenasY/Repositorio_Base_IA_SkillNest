import json
import re


def parsear_respuesta_json(texto, claves_esperadas=None):
    """Limpia y convierte en dict la respuesta JSON de un modelo.

    Quita las marcas ```json ... ``` que a veces envuelven la respuesta
    y valida que contenga las claves esperadas. Si no se indican claves,
    se validan 'categoria' y 'confianza'.
    """
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)

    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")

    if claves_esperadas is None:
        claves_esperadas = ["categoria", "confianza"]

    for clave in claves_esperadas:
        if clave not in datos:
            raise ValueError("La respuesta no tiene la estructura esperada.")

    return datos
