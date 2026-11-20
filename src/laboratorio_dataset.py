import os
import json
import time
from collections import Counter
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

#Paso 1: Construcción de Dataset
ejemplos_raw = [
    ("TimeoutError: la conexion tardo mas de 10 segundos en responder.",#text_input
     {"categoria": "red", "accion_sugerida": "reintentar con backoff exponencial"}), #output
    ("ValueError: la clave de API no tiene el formato esperado.",
     {"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
    ("429 RESOURCE_EXHAUSTED: se supero el limite de peticiones por minuto.",
     {"categoria": "cuota", "accion_sugerida": "esperar y reintentar, con backoff"}),
    ("API key not valid. Please pass a valid API key.",
     {"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
    ("RuntimeError: Your system has an unsupported version of sqlite3.",
     {"categoria": "entorno", "accion_sugerida": "instalar pysqlite3-binary"}),
    ("ModuleNotFoundError: No module named langchain_chroma.",
     {"categoria": "entorno", "accion_sugerida": "instalar dependencia faltante"}),
    ("PermissionError al crear la carpeta del vector store.",
     {"categoria": "entorno", "accion_sugerida": "revisar permisos de escritura"}),
    ("InvalidArgumentError: Collection expecting embedding with dimension of 768, got 1536.",
     {"categoria": "consistencia_indice", "accion_sugerida": "reindexar con el mismo modelo de embeddings"}),
]

#Contruyendo una lista de objetos TuningExample usando texto como text_input y salida como output
examples = [
    types.TuningExample(text_input=texto, output=json.dumps(salida, ensure_ascii=False))
    for texto, salida in ejemplos_raw
]

def validar_dataset(examples, claves_esperadas=("categoria", "accion_sugerida")):
    problemas = []
    vistos = set()
    for i, ej in enumerate(examples):
        if not ej.text_input or not ej.text_input.strip():
            problemas.append(f"ejemplo {i}: text_input vacio")
        if not ej.output or not ej.output.strip():
            problemas.append(f"ejemplo {i}: output vacio")
            continue
        if ej.text_input in vistos:
            problemas.append(f"ejemplo {i}: text_input duplicado")
        vistos.add(ej.text_input)
        try:
            salida = json.loads(ej.output)
        except json.JSONDecodeError:
            problemas.append(f"ejemplo {i}: output no es JSON valido")
            continue
        for clave in claves_esperadas:
            if clave not in salida:
                problemas.append(f'ejemplo {i}: output no tiene la clave "{clave}"')
    return problemas

def esperar_a_que_termine(client: genai.Client, nombre_trabajo: str, intervalo_segundos: int = 30) -> types.TuningJob:
    estados_finales = {
        types.JobState.JOB_STATE_SUCCEEDED,
        types.JobState.JOB_STATE_FAILED,
        types.JobState.JOB_STATE_CANCELLED,
        types.JobState.JOB_STATE_PARTIALLY_SUCCEEDED,
    }
    while True:
        trabajo = client.tunings.get(name=nombre_trabajo)
        print(f"Estado actual: {trabajo.state}")
        if trabajo.state in estados_finales:
            return trabajo
        time.sleep(intervalo_segundos)

def chequear_balance(ejemplos_raw):
    categorias = Counter(salida["categoria"] for _, salida in ejemplos_raw)
    return categorias

if __name__ == "__main__":
    #Validación del Dataset

    #Chequeo de Balance

    cliente = genai.Client(
        vertexai=True,
        project="project-87ac4e31-4117-499a-944",
        location="us-central1"
    )

#TrainingDataset URI
    dataset = types.TuningDataset(gcs_uri="gs://bucket_first_ai/ejemplos_tuning.jsonl")

    config = types.CreateTuningJobConfig(
        tuning_mode=types.TuningMode.TUNING_MODE_PEFT_ADAPTER,
        adapter_size=types.AdapterSize.ADAPTER_SIZE_FOUR,
        epoch_count=5,
        tuned_model_display_name="categorizacion-errores"
    )

    try:
        print("Iniciando el proceso de tuning con Google AI!")
        trabajo = cliente.tunings.tune(
            base_model="gemini-2.5-flash",
            training_dataset=dataset,
            config=config,
        )

        print(f"Trabajo de tuning creado con éxtito: {trabajo.name}")

        resultado_final = esperar_a_que_termine(cliente, trabajo.name)
        print(f"\n Proceso finalizado con estado:", {resultado_final.state})

        if resultado_final.state == types.JobState.JOB_STATE_SUCCEEDED:
            print("Modelo listo para usar: ", resultado_final.tuned_model)

    except Exception as error:
        print(f"Error durante el proceso de tuning: {error}")


