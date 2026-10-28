"""
Uso:
    python app.py
    python app.py "¿Cuál es la capital de Chile?"

    """

import sys
from pathlib import Path

# Los módulos de src/ usan imports _planos_ (from armar_peticion import ...),
# por lo que hay que agregar esa carpeta al path para poder importarlos.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from armar_peticion import armar_peticion
from consulta_y_consumo import enviar_peticion, extraer_texto, calcular_costo

# Pregunta por defecto cuando no se pasan argumentos por la línea de comandos.
PREGUNTA_POR_DEFECTO = "¿Cuál es la capital de Chile?"

# Precios por token en USD (mismos valores usados en src/consumir_gemini.py).
PRECIO_ENTRADA = 0.00000010
PRECIO_SALIDA = 0.00000030


def main():
    """Hace la consulta a Gemini y muestra la respuesta y el costo estimado."""

    pregunta = " ".join(sys.argv[1:]).strip() or PREGUNTA_POR_DEFECTO

    # Paso 1: preparar la petición (URL + body) con la key y el modelo del .env.
    url, body = armar_peticion(pregunta)

    # Paso 2: enviar la petición a Gemini y quedarnos con el JSON de respuesta.
    datos = enviar_peticion(url, body)

    # Paso 3: de toda la respuesta, sacar solamente el texto del modelo.
    texto = extraer_texto(datos)

    # Paso 4: estimar el costo con los tokens que informa la respuesta.
    costo = calcular_costo(datos, PRECIO_ENTRADA, PRECIO_SALIDA)

    print(f"Pregunta: {pregunta}")
    print("\nRespuesta de Gemini:")
    print(texto)
    print(f"\nCosto estimado de la consulta: ${costo:.6f} USD")

    # Devolvemos el texto por si más adelante se quiere reutilizar.
    return texto


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as error:
        # enviar_peticion incluye la URL (con la key) en el mensaje de error:
        # se recorta para no exponer la llave en la salida.
        mensaje = str(error).split("?key=")[0]
        print(f"\nNo se pudo completar la consulta: {mensaje}")
