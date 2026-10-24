import time

from armar_peticion import armar_peticion
from consulta_y_consumo import enviar_peticion, calcular_costo

PRECIO_ENTRADA = 0.00000010  # el valor real de la página de precios
PRECIO_SALIDA = 0.00000030


def medir_latencia_y_costo(pregunta):
    """Mide la latencia promedio y el costo de la última petición."""
    latencias = []
    respuesta_json = None

    for i in range(4):
        url, body = armar_peticion(pregunta)
        inicio = time.perf_counter()
        respuesta_json = enviar_peticion(url, body)
        fin = time.perf_counter()

        latencias.append(fin - inicio)
        print(f"Intento {i + 1}: {latencias[-1]:.2f} segundos")

    latencia_promedio = sum(latencias) / len(latencias)
    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")

    costo = calcular_costo(respuesta_json, PRECIO_ENTRADA, PRECIO_SALIDA)
    print(f"Costo de la última petición: {costo}")

    return respuesta_json


if __name__ == "__main__":
    pregunta = "clima de Arica, Chile mañana"
    medir_latencia_y_costo(pregunta)
