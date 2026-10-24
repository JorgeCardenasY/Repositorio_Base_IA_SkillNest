import sys
from pathlib import Path

# Hacer visible la raíz del proyecto para poder importar la carpeta "prompts"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import time
from parsear_respuesta import parsear_respuesta_json
from prompts.banco import BANCO_DE_PROMPT
from armar_peticion import armar_peticion
from consulta_y_consumo import enviar_peticion, extraer_texto

# Ruta absoluta: funciona desde cualquier directorio de trabajo
RUTA_REGISTRO = Path(__file__).resolve().parents[1] / "prompts" / "registro.json"

registro = {}

try:

    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        intentos = 3
        for intento in range(intentos):
            url, body = armar_peticion(
                prompt["ejemplo_usuario"],
                prompt["system_instruction"],
                prompt["response_schema"],
            )
            respuesta = enviar_peticion(url, body)
            texto = extraer_texto(respuesta)
            try:
                datos = parsear_respuesta_json(texto, prompt["claves_esperadas"])
                exitos += 1
                print(f"Respuesta: {datos}")
            except ValueError as error:
                print(f"Error en el intento {intento + 1}: {error}")
                time.sleep(1)
        print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas")
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
        with open(RUTA_REGISTRO, "w", encoding="utf-8") as archivo:
            json.dump(registro, archivo, indent=2, ensure_ascii=False)
    

except(ValueError, RuntimeError) as error:
    print("No se pudo completar la petición debido a un error:", error)