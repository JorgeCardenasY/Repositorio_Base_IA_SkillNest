import re

from collections import Counter

def limpiar_texto(texto: str) -> str:
    """Normaliza el texto: minúsculas y sin puntuación."""
    if not isinstance(texto, str):
        tipo = type(texto).__name__
        raise TypeError(f"limpiar_texto espera str, no {tipo}")

    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def tokenizar(texto_limpio: str) -> list[str]:
    """Convierte texto limpio en una lista de tokens."""
    return texto_limpio.split()

def vectorizar(tokens: list[str]) -> Counter:
    """Cuenta cuántas veces aparece cada token."""
    return Counter(tokens)

def procesar_texto(texto):
    texto_limpio = limpiar_texto(texto)
    return tokenizar(texto_limpio)

if __name__ == "__main__":
     texto = "Santiago es la capital de Chile. ¡Santiago es horrible!"
"""
    texto_limpio = limpiar_texto(texto)

    tokens = tokenizar(texto_limpio)

    conteo = vectorizar(tokens)

#    print("Texto limpio:", texto_limpio)
#    print("Tokens:", tokens)

    print("Conteo:", conteo)

    print("Texto limpio:", procesar_texto(texto)) """

referencia = "El perro persiguió al gato."

respuesta = "El gato persiguió al perro."


tokens_referencia = procesar_texto(referencia)

tokens_respuesta = procesar_texto(respuesta)


comunes = set(tokens_referencia) & set(tokens_respuesta)

if tokens_referencia:
    proporcion = len(comunes) / len(set(tokens_referencia))
else:
    proporcion = 0.0

print(f"Coincidencia: {proporcion:.0%}")