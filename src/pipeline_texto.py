"""Consulta mínima a Gemini y comparación de coincidencia de texto.

El import de ``cliente`` es perezoso (dentro de ``consultar_texto``) para que
importar este módulo no cargue el ``.env`` ni ``requests`` ni gaste cuota: la
consulta solo ocurre al ejecutar el bloque ``__main__``.
"""

from pipeline import procesar_texto


def consultar_texto(pregunta: str) -> str:
    """Consulta mínima: devuelve el texto del modelo para ``pregunta``.

    El import se hace aquí dentro, y no en la cabecera, para que importar este
    módulo no cargue el ``.env`` ni ``requests`` ni gaste cuota: la consulta a
    Gemini solo ocurre al ejecutar el bloque ``__main__``.
    """
    from cliente import consultar_modelo

    return consultar_modelo(pregunta)


if __name__ == "__main__":
    consulta = "¿Qué es Python?"

    referencia = "Python interpretado."

    respuesta = consultar_texto(consulta)


    crudo_ref = referencia.split()

    crudo_resp = respuesta.split()

    comunes_crudo = set(crudo_ref) & set(crudo_resp)

    pct_crudo = len(comunes_crudo) / len(set(crudo_ref))


    tokens_ref = procesar_texto(referencia)

    tokens_resp = procesar_texto(respuesta)

    comunes = set(tokens_ref) & set(tokens_resp)

    pct_proc = len(comunes) / len(set(tokens_ref))


    print(f"[Caso 1] Coincidencia texto crudo: {pct_crudo:.1%}")

    print(f"[Caso 1] Coincidencia texto procesado: {pct_proc:.1%}")
