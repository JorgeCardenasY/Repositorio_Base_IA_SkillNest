"""Evaluacion de coincidencia entre una referencia y una respuesta de ejemplo.

El bloque ``__main__`` solo calcula y muestra la coincidencia de texto crudo y
procesado, sin consultar al modelo, para que la salida sea reproducible:

    [Caso 1] Coincidencia texto crudo: 57.1%
    [Caso 1] Coincidencia texto procesado: 100.0%

``consultar_texto`` queda disponible para obtener respuestas reales: importa
``cliente.consultar_modelo`` dentro de la funcion para que importar este
modulo no cargue el ``.env`` ni ``requests`` ni gaste cuota.
"""

from pipeline import procesar_texto


def consultar_texto(pregunta: str) -> str:
    """Consulta mínima: devuelve el texto del modelo para ``pregunta``."""
    from cliente import consultar_modelo

    return consultar_modelo(pregunta)


if __name__ == "__main__":
    referencia = "Python fue creado en 1991 por Guido van Rossum."
    respuesta = (
    "Python fue creado en 1989 por Guido van Rossum, "
    "pensado como sucesor de ABC."
    )



"""
Se comentan para probar nueva línea de código:

    referencia = "Python es un de programación interpretado."

    respuesta = "**Python** es un **lenguaje** de *programación*, interpretado."
"""

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
