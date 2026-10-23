"""
Este archivo hace UNA pregunta al LLM (actualmente , GEMINI) y guarda 
la respuesta "ordenada" en un diccionario de Python, pares {clave:valor}.

Se utilizan funciones que ya están hechas en este mismo proyecto (no
escribimos la conexión a internet desde cero).

"""

# ---------------------------------------------------------------------------
# PASO 0: Variables de Ambiente (API key desde fichero .env)
# ---------------------------------------------------------------------------
# Es relevante mencionar que el archivo .env es un almacén para variables
# de entorno. Ahí configuramps el valor de la API key (la "llave" que nos 
# permite conectar para consultar a Gemini). Es importante señalar que esta
# llave NO se escribe dentro del código (no se _hardcodea_), porque el
# código se comparte y la llave quedaría expuesta.
#
# load_dotenv() permite la carga de las variables de ambiente para usarlas.
from pathlib import Path
from dotenv import load_dotenv

# __file__ es este mismo archivo. Path(...) construye la ruta hasta el .env.
# Como este archivo está dentro de src/, subimos una carpeta (parents[1])
# para encontrar el .env en la raíz del proyecto.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# ---------------------------------------------------------------------------
# PASO 1: traer las funciones que ya existen en el proyecto
# ---------------------------------------------------------------------------
# Importaremos las funciones que ya están hechas en otros 
# archivos de este proyecto.
#
# armar_peticion: 'prepara' la solicitud que le vamos a mandar a Gemini.
#

from armar_peticion import armar_peticion

# enviar_peticion: manda el request y trae la respuesta.
# extraer_texto:   de toda la respuesta, saca sólo el texto que escribió
#                  el modelo (lo demás es información técnica o metadatos
#                  que no usamos).

from consulta_y_consumo import enviar_peticion, extraer_texto

# parsear_respuesta_json: toma ese texto y lo convierte en un diccionario.

from parsear_respuesta import parsear_respuesta_json

# ---------------------------------------------------------------------------
# PASO 2: escribir las instrucciones para el asistente
# ---------------------------------------------------------------------------
# Esta configuración permite que el modelo sepa cómo debe responder.
# 
# Le pedimos JSON porque es un formato ordenado y estructurado estándar
# para la comunicación entre máquinas.

SYSTEM_INSTRUCTION = """
Eres un asistente técnico. Responde SIEMPRE en formato JSON válido,
sin texto antes ni después, usando exactamente estas claves:
- "categoria": tema principal de la pregunta (texto corto).
- "confianza": qué tan seguro estás, número entero de 0 a 100.
- "explicacion": tu respuesta, en un máximo de 3 oraciones.
No agregues bloques de código ni comentarios fuera del JSON.
"""

# La pregunta que queremos hacerle al modelo.
PREGUNTA = "relaciona Tecnofeudalismo y el concepto del 'esclavitud asalariada' 'de Diego fusaro'"

# ---------------------------------------------------------------------------
# PASO 3: describir cómo queremos que venga la respuesta
# ---------------------------------------------------------------------------
# Esto es la "plantilla" de la ficha. Al entregársela a Gemini, el modelo
# queda obligado a responder respetando esos campos.
#
# - "OBJECT"  significa: la respuesta es una ficha con datos por dentro.
# - "STRING"  significa: ese campo lleva texto.
# - "INTEGER" significa: ese campo lleva un número entero.
# - "required" es la lista de campos que NO pueden faltar.
RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "categoria": {"type": "STRING"},
        "confianza": {"type": "INTEGER"},
        "explicacion": {"type": "STRING"},
    },
    "required": ["categoria", "confianza", "explicacion"],
}

# Estos son los nombres de los campos que revisará la función parsear_respuesta_json:
# Si al modelo se le olvida uno, la función avisa con un error.
CLAVES_ESPERADAS = ["categoria", "confianza", "explicacion"]


def main():
    """Hace la consulta y muestra la respuesta ya ordenada."""

    # Paso 1: preparar el request (la URL y los datos que se enviarán).
    # Aquí dentro se usan la API key y el modelo que vienen del .env.
    url, body = armar_peticion(PREGUNTA, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)

    # Paso 2: enviar el request a Gemini y quedarnos con su respuesta.
    respuesta_json = enviar_peticion(url, body)

    # Paso 3: de toda la respuesta, sacar solamente el texto del modelo.
    texto = extraer_texto(respuesta_json)

    print("Respuesta tal cual la escribió el modelo:")
    print(texto)

    # Paso 4: convertir ese texto en un diccionario de Python.
    # Si el modelo lo entregó envuelto en ```json ... ```, esta función
    # le quita esa "envoltura" antes de convertirlo.
    datos = parsear_respuesta_json(texto, CLAVES_ESPERADAS)

    # Mostramos la ficha campo por campo, para que se entienda mejor.
    print("\nRespuesta ordenada en campos:")
    for nombre, valor in datos.items():
        print(f"  {nombre}: {valor}")

    #print("\n¿Qué tipo de dato es 'datos'?:", type(datos).__name__)

    # Devolvemos el diccionario por si más adelante queremos usarlo.
    return datos


if __name__ == "__main__":
    # Si algo sale mal (no hay internet, la clave no sirve, el modelo
    # respondió algo que no era JSON...), mostramos un aviso entendible
    # en vez de un error enorme y difícil de leer.
    try:
        main()
    except (ValueError, RuntimeError) as error:
        print(f"\nNo se pudo completar la consulta: {error}")
