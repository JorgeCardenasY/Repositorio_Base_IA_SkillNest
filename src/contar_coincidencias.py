"""Conteo de coincidencias y métricas de precisión, cobertura y F1.

Compara los tokens de una referencia con los de una respuesta del modelo.
``calcular_metricas`` procesa ambos textos y devuelve las tres métricas.

Uso:
    python src/contar_coincidencias.py

El bloque ``__main__`` ejecuta tres casos de ejemplo; cada caso hace una
consulta real a Gemini y consume cuota. Importar este módulo no consulta al
modelo ni imprime nada.
"""

from collections import Counter

from cliente import consultar_modelo
from pipeline import procesar_texto


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


def calcular_metricas(
    texto_referencia: str,
    texto_respuesta: str,
) -> dict[str, float]:
    """Procesa ambos textos y devuelve precisión, cobertura y F1."""
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )


casos = [
    (
        "¿Qué es Python?",
        "Python es un lenguaje de programación interpretado.",
    ),
    ("¿Cuándo se creó Python?", "Python fue creado en 1991."),
    (
        "¿Qué es una lista en Python?",
        "Una lista es una colección ordenada y modificable.",
    ),
]


def main() -> None:
    """Ejecuta los casos de ejemplo contra el modelo."""
    for consulta, referencia in casos:
        try:
            respuesta = consultar_modelo(consulta)
        except (RuntimeError, ValueError) as error:
            print(f"{consulta} -> error: {error}")
            continue
        metricas = calcular_metricas(referencia, respuesta)
        print(f"{consulta} -> {metricas}")


if __name__ == "__main__":
    main()


##

import json


resultados = []

for consulta, referencia in casos:

    respuesta = consultar_modelo(consulta)

    metricas = calcular_metricas(referencia, respuesta)

    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })


with open(
    "src/resultados_metricas.json", "w", encoding="utf-8"
) as archivo:

    json.dump(resultados, archivo, indent=2, ensure_ascii=False)



def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }

peores_casos = sorted(resultados, key=lambda r: r["f1"])

for caso in peores_casos[:3]:

    print(caso["consulta"], caso["f1"])