"""Conteo de coincidencias y métricas de precisión, cobertura y F1.

El bloque ``__main__`` compara dos frases de ejemplo con ``procesar_texto``
(limpieza y tokenización de ``pipeline.py``) y muestra el resultado:

    Coincidencias: 5
    Precisión: 55.6%
    Cobertura: 83.3%
    F1: 66.7%

No consulta al modelo ni gasta cuota.
"""

from collections import Counter


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta los tokens comunes respetando las repeticiones."""
    return sum(
        (Counter(tokens_referencia) & Counter(tokens_respuesta)).values()
    )


def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    return {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }


if __name__ == "__main__":
    from pipeline import procesar_texto

    """    
    referencia = "Python es un lenguaje de programación interpretado."
    respuesta = "¿Qué es Python?"
    """
    
    referencia = "El auto es veloz."
    respuesta = "El vehículo es rápido."

    tokens_referencia = procesar_texto(referencia)
    tokens_respuesta = procesar_texto(respuesta)

    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )
    metricas = calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

"""     print(f"Coincidencias: {coincidencias}")
    print(f"Precisión: {metricas['precision']:.1%}")
    print(f"Cobertura: {metricas['cobertura']:.1%}")
    print(f"F1: {metricas['f1']:.1%}") """


resultado = calcular_precision_cobertura_f1(referencia, respuesta)

print(resultado)