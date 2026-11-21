"""Conteo de coincidencias y métricas de precisión, cobertura y F1.

Compara los tokens de una referencia con los de una respuesta del modelo.
``calcular_metricas`` procesa ambos textos y devuelve las tres métricas.

Uso:
    python src/contar_coincidencias.py

El bloque ``__main__`` consulta al modelo una vez por caso del dataset de
evaluación, calcula sus métricas y guarda el resultado en
``src/resultados_metricas.json`` (una escritura por caso, para no perder la
corrida si el proveedor corta por cuota). Importar este módulo no consulta al
modelo ni escribe archivos.
"""

import json
import time
from collections import Counter
from pathlib import Path

from cliente import consultar_modelo
from pipeline import procesar_texto

SALIDA = Path(__file__).with_name("resultados_metricas.json")
PAUSA_SEGUNDOS = 3
BREVE = "Responde en una sola frase, sin listas ni markdown."


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


# Dataset de evaluación: (consulta, referencia[, system_instruction]).
# Los casos sin instrucción producen respuestas largas y los marcados con
# BREVE, respuestas de una sola frase. Ese contraste es el que se revisa a
# mano en docs/limites_metrica.md.
casos: list[tuple] = [
    # --- respuestas largas, sin instrucción ---
    (
        "¿Qué es Python?",
        "Python es un lenguaje de programación interpretado.",
    ),
    ("¿Cuándo se creó Python?", "Python fue creado en 1991."),
    (
        "¿Qué es una lista en Python?",
        "Una lista es una colección ordenada y modificable.",
    ),
    (
        "Explícame con detalle qué es una tupla en Python.",
        "Una tupla es una colección ordenada e inmutable.",
    ),
    (
        "Explícame con detalle qué es un diccionario en Python.",
        "Un diccionario es una colección de pares clave-valor.",
    ),
    # --- respuestas de una frase (instrucción de brevedad) ---
    (
        "¿Qué es una tupla en Python?",
        "Una tupla es una colección ordenada e inmutable.",
        BREVE,
    ),
    (
        "¿Qué es un diccionario en Python?",
        "Un diccionario es una colección de pares clave-valor.",
        BREVE,
    ),
    (
        "¿Qué hace la función len() en Python?",
        "len() devuelve la cantidad de elementos de una secuencia.",
        BREVE,
    ),
    (
        "¿Qué hace el método append() en una lista?",
        "append() agrega un elemento al final de la lista.",
        BREVE,
    ),
    ("¿Qué es pip?", "pip es el gestor de paquetes de Python.", BREVE),
    (
        "¿Qué es un módulo en Python?",
        "Un módulo es un archivo con código Python reutilizable.",
        BREVE,
    ),
    (
        "¿Qué hace la función range() en Python?",
        "range() genera una secuencia de números.",
        BREVE,
    ),
    (
        "¿Qué es un entorno virtual en Python?",
        "Un entorno virtual aísla las dependencias de un proyecto.",
        BREVE,
    ),
    # --- datos verificables: fecha, versión, nombre propio ---
    (
        "¿Quién creó Python?",
        "Python fue creado por Guido van Rossum.",
        BREVE,
    ),
    (
        "¿En qué año se lanzó Python 3.0?",
        "Python 3.0 se lanzó en 2008.",
        BREVE,
    ),
    (
        "¿En qué año se publicó la primera versión de Python?",
        "La primera versión pública fue Python 0.9.0, en 1991.",
        BREVE,
    ),
    (
        "¿En qué año terminó el soporte oficial de Python 2?",
        "El soporte de Python 2 terminó el 1 de enero de 2020.",
        BREVE,
    ),
    (
        "¿Qué versión de Python introdujo los f-strings?",
        "Los f-strings se introdujeron en Python 3.6.",
        BREVE,
    ),
    # --- respuestas de si/no con negación ---
    (
        "¿Python es de tipado estático?",
        "No, Python es de tipado dinámico.",
        BREVE,
    ),
    (
        "¿Se puede modificar una tupla después de crearla en Python?",
        "No, una tupla es inmutable.",
        BREVE,
    ),
    (
        "¿Python se compila a código máquina antes de ejecutarse?",
        "No, Python se ejecuta mediante un intérprete.",
        BREVE,
    ),
    (
        "¿Una lista en Python puede contener elementos de distintos tipos?",
        "Sí, una lista puede contener elementos de distintos tipos.",
        BREVE,
    ),
]


def generar_resultados(casos: list[tuple], salida: Path = SALIDA) -> list[dict]:
    """Consulta el modelo caso por caso y guarda el JSON tras cada respuesta."""
    resultados: list[dict] = []

    for consulta, referencia, *resto in casos:
        instruccion = resto[0] if resto else ""
        try:
            respuesta = consultar_modelo(consulta, instruccion)
        except (RuntimeError, ValueError) as error:
            print(f"{consulta} -> error: {error}")
            continue

        metricas = calcular_metricas(referencia, respuesta)
        resultados.append({
            "consulta": consulta,
            "respuesta": respuesta,
            **metricas,
        })

        with open(salida, "w", encoding="utf-8") as archivo:
            json.dump(resultados, archivo, indent=2, ensure_ascii=False)

        print(f"{consulta} -> f1={metricas['f1']:.3f}")
        time.sleep(PAUSA_SEGUNDOS)

    return resultados


def resumir_metricas(resultados: list[dict]) -> dict[str, float]:
    """Devuelve el promedio de cada métrica sobre los resultados dados."""
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


def main() -> None:
    """Genera las métricas de todo el dataset y guarda el JSON."""
    resultados = generar_resultados(casos)
    resumen = resumir_metricas(resultados)

    print(f"\n{len(resultados)} casos guardados en {SALIDA.name}")
    print(f"f1 promedio: {resumen['f1_promedio']:.3f}")

    peores_casos = sorted(resultados, key=lambda r: r["f1"])
    for caso in peores_casos[:3]:
        print(f"peor f1: {caso['consulta']} -> {caso['f1']:.3f}")

    if len(resultados) < 20:
        raise SystemExit(
            f"Se esperaban al menos 20 casos y se guardaron {len(resultados)}"
        )


if __name__ == "__main__":
    main()
