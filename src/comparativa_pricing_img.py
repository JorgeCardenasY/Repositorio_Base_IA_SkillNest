"""Comparativa de precios, latencia y reconocimiento de placa patente.

Envía una imagen PNG a Gemini y DeepSeek para extraer los caracteres de
una placa patente (matrícula) y genera una tabla comparativa de:
- Placa extraída
- Costo por 1000 tokens de entrada
- Costo por 1000 tokens de salida
- Latencia observada
- Fecha de medición

Para Gemini utiliza el modelo configurado en el repositorio
(modelo="gemini-flash-latest"). Para DeepSeek utiliza los modelos
configurados en .env (modelo_DS_Pro y modelo_DS_Flash) y la API oficial
de DeepSeek a través del SDK de OpenAI.

Uso: python src/comparativa_pricing.py [ruta/imagen.png]
"""

import base64
import os
import sys
import time
from datetime import date

from dotenv import load_dotenv
from openai import OpenAI, BadRequestError

from consulta_y_consumo import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    calcular_costo,
)

# Cargar variables de entorno desde .env
load_dotenv()

# ---------------------------------------------------------------------------
# Precios por token (USD)
# ---------------------------------------------------------------------------
# Gemini (gemini-flash-latest): valores ya usados en src/consumir_gemini.py
PRECIO_ENTRADA_GEMINI = 0.00000010
PRECIO_SALIDA_GEMINI = 0.00000030

# DeepSeek PRO (deepseek-v4-pro) — cache miss, peak (off-peak = mitad).
# Entrada: $1.32 / 1M tokens  -> 1.32e-6 por token
# Salida:  $3.96 / 1M tokens  -> 3.96e-6 por token
PRECIO_ENTRADA_DEEPSEEK_PRO = 0.00000132
PRECIO_SALIDA_DEEPSEEK_PRO = 0.00000396

# DeepSeek Flash (deepseek-flash) — cache miss, peak (off-peak = mitad).
# Entrada: $0.30 / 1M tokens  -> 3.0e-7 por token
# Salida:  $1.20 / 1M tokens  -> 1.2e-6 por token
PRECIO_ENTRADA_DEEPSEEK_FLASH = 0.00000030
PRECIO_SALIDA_DEEPSEEK_FLASH = 0.00000120


def codificar_imagen(ruta):
    """Lee un archivo de imagen y devuelve su contenido en base64."""
    with open(ruta, "rb") as archivo:
        return base64.b64encode(archivo.read()).decode("utf-8")


def consultar_gemini(pregunta, imagen_base64=None):
    """Consulta Gemini y devuelve latencia, tokens, costo y placa extraída."""
    url, body = armar_peticion(pregunta, imagen_base64)

    inicio = time.perf_counter()
    datos = enviar_peticion(url, body)
    fin = time.perf_counter()

    latencia = fin - inicio

    uso = datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_total = uso["totalTokenCount"]

    costo = calcular_costo(datos, PRECIO_ENTRADA_GEMINI, PRECIO_SALIDA_GEMINI)
    placa = extraer_texto(datos)

    return {
        "modelo": os.getenv("modelo", "gemini-flash-latest"),
        "latencia": latencia,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "tokens_total": tokens_total,
        "costo": costo,
        "placa": placa,
        "estado": "ok",
    }


def consultar_deepseek(
    pregunta, modelo, precio_entrada, precio_salida, imagen_base64=None
):
    """Consulta un modelo de DeepSeek usando el SDK de OpenAI.

    Normaliza la respuesta (response.usage) al formato usageMetadata para
    reutilizar calcular_costo de consulta_y_consumo. Si se proporciona una
    imagen, se envía en formato multimodal (image_url).
    """
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    if imagen_base64:
        contenido = [
            {"type": "text", "text": pregunta},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{imagen_base64}"},
            },
        ]
    else:
        contenido = pregunta

    inicio = time.perf_counter()
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": contenido},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )
    fin = time.perf_counter()

    latencia = fin - inicio

    uso = response.usage
    if uso is None:
        raise RuntimeError("La respuesta de DeepSeek no incluye datos de uso.")

    tokens_entrada = uso.prompt_tokens
    tokens_salida = uso.completion_tokens
    tokens_total = uso.total_tokens

    # Normalizamos al formato que espera calcular_costo (usageMetadata).
    datos_normalizados = {
        "usageMetadata": {
            "promptTokenCount": tokens_entrada,
            "candidatesTokenCount": tokens_salida,
            "totalTokenCount": tokens_total,
        }
    }
    costo = calcular_costo(datos_normalizados, precio_entrada, precio_salida)
    placa = response.choices[0].message.content

    return {
        "modelo": modelo,
        "latencia": latencia,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "tokens_total": tokens_total,
        "costo": costo,
        "placa": placa,
        "estado": "ok",
    }


def imprimir_metricas(titulo, resultado):
    """Imprime las métricas observadas para un modelo."""
    print(f"\n--- {titulo} ({resultado['modelo']}) ---")
    print(f"Placa extraída: {resultado['placa']}")
    print(f"Tokens de entrada: {resultado['tokens_entrada']}")
    print(f"Tokens de salida: {resultado['tokens_salida']}")
    print(f"Total: {resultado['tokens_total']}")
    print(f"Costo de la operación: ${resultado['costo']:.6f} USD")
    print(f"Latencia: {resultado['latencia']:.2f} segundos")


def formato_usd(valor):
    """Formatea un monto en USD sin ceros finales innecesarios."""
    texto = f"{valor:.6f}".rstrip("0").rstrip(".")
    return f"${texto}"



def generar_tabla(resultados):
    """Genera la tabla Markdown comparativa de los tres modelos.

    resultados: lista de dicts con claves etiqueta, resultado,
    precio_entrada y precio_salida. El dict resultado incluye estado,
    placa y latencia (o None si el modelo no soporta la consulta).
    """
    hoy = date.today().isoformat()

    lineas = []
    lineas.append("| CRITERIO | MODELO 'GEMINI' | DeepSeek PRO | DeepSeek Flash |")
    lineas.append("|---|---|---|---|")

    def valor_celda(resultado, campo):
        res = resultado["resultado"]
        if res.get("estado") == "ok":
            return str(res.get(campo) or "N/A")
        return res.get("estado") or "Error"

    placas = [valor_celda(e, "placa") for e in resultados]
    lineas.append(
        f"| Placa extraída | {placas[0]} | {placas[1]} | {placas[2]} |"
    )

    entradas_tokens = [valor_celda(e, "tokens_entrada") for e in resultados]
    lineas.append(
        f"| Tokens entrada CONSUMIDOS | {entradas_tokens[0]} | {entradas_tokens[1]} | {entradas_tokens[2]} |"
    )

    salidas_tokens = [valor_celda(e, "tokens_salida") for e in resultados]
    lineas.append(
        f"| Tokens Salida CONSUMIDOS | {salidas_tokens[0]} | {salidas_tokens[1]} | {salidas_tokens[2]} |"
    )

    entradas = [formato_usd(e["precio_entrada"] * 1000) for e in resultados]
    lineas.append(
        f"| Costo por 1000 tokens de entrada | {entradas[0]} | {entradas[1]} | {entradas[2]} |"
    )

    salidas = [formato_usd(e["precio_salida"] * 1000) for e in resultados]
    lineas.append(
        f"| Costo por 1000 tokens de Salida | {salidas[0]} | {salidas[1]} | {salidas[2]} |"
    )

    def celda_costo(res):
        if res.get("estado") == "ok":
            return formato_usd(res.get("costo", 0.0))
        return res.get("estado") or "Error"

    totales = [celda_costo(e["resultado"]) for e in resultados]
    lineas.append(
        f"| Total de la Consulta | {totales[0]} | {totales[1]} | {totales[2]} |"
    )

    latencias = []
    for e in resultados:
        res = e["resultado"]
        if res.get("estado") == "ok":
            latencias.append(f"{res['latencia']:.2f} s")
        else:
            latencias.append(res.get("estado") or "Error")
    lineas.append(
        f"| Latencia Observada | {latencias[0]} | {latencias[1]} | {latencias[2]} |"
    )

    lineas.append(f"| Fecha de Medición | {hoy} | {hoy} | {hoy} |")

    return "\n".join(lineas)


def main():
    # Ruta de la imagen PNG: primer argumento o un valor por defecto.
    ruta_imagen = sys.argv[1] if len(sys.argv) > 1 else "placa.png"

    try:
        imagen_base64 = codificar_imagen(ruta_imagen)
    except FileNotFoundError:
        print(f"No se encontró la imagen: {ruta_imagen}")
        sys.exit(1)

    pregunta = (
        "Extrae únicamente los caracteres de la placa patente (matrícula) "
        "que aparece en la imagen. Responde solo con el texto de la placa, "
        "sin comentarios adicionales."
    )

    print("=" * 72)
    print("COMPARATIVA: GEMINI vs DEEPSEEK PRO vs DEEPSEEK FLASH")
    print(f"Imagen analizada: {ruta_imagen}")
    print("=" * 72)

    resultados = []

    def entrada_fallo(modelo, estado):
        return {
            "modelo": modelo,
            "estado": estado,
            "placa": None,
            "latencia": None,
        }

    # 1) Gemini
    try:
        resultado = consultar_gemini(pregunta, imagen_base64)
        imprimir_metricas("Gemini", resultado)
        resultados.append({
            "etiqueta": "MODELO 'GEMINI'",
            "resultado": resultado,
            "precio_entrada": PRECIO_ENTRADA_GEMINI,
            "precio_salida": PRECIO_SALIDA_GEMINI,
        })
    except Exception as error:
        print(f"\nError consultando Gemini: {error}")
        resultados.append({
            "etiqueta": "MODELO 'GEMINI'",
            "resultado": entrada_fallo("gemini-flash-latest", "Error"),
            "precio_entrada": PRECIO_ENTRADA_GEMINI,
            "precio_salida": PRECIO_SALIDA_GEMINI,
        })

    # 2) DeepSeek PRO
    modelo_pro = os.getenv("modelo_DS_Pro", "deepseek-v4-pro")
    try:
        resultado = consultar_deepseek(
            pregunta,
            modelo_pro,
            PRECIO_ENTRADA_DEEPSEEK_PRO,
            PRECIO_SALIDA_DEEPSEEK_PRO,
            imagen_base64,
        )
        imprimir_metricas("DeepSeek PRO", resultado)
        resultados.append({
            "etiqueta": "DeepSeek PRO",
            "resultado": resultado,
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_PRO,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_PRO,
        })
    except BadRequestError as error:
        print(f"\nDeepSeek PRO no soporta imágenes: {error}")
        resultados.append({
            "etiqueta": "DeepSeek PRO",
            "resultado": entrada_fallo(modelo_pro, "No soporta visión"),
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_PRO,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_PRO,
        })
    except Exception as error:
        print(f"\nError consultando DeepSeek PRO: {error}")
        resultados.append({
            "etiqueta": "DeepSeek PRO",
            "resultado": entrada_fallo(modelo_pro, "Error"),
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_PRO,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_PRO,
        })

    # 3) DeepSeek Flash
    modelo_flash = os.getenv("modelo_DS_Flash", "deepseek-flash")
    try:
        resultado = consultar_deepseek(
            pregunta,
            modelo_flash,
            PRECIO_ENTRADA_DEEPSEEK_FLASH,
            PRECIO_SALIDA_DEEPSEEK_FLASH,
            imagen_base64,
        )
        imprimir_metricas("DeepSeek Flash", resultado)
        resultados.append({
            "etiqueta": "DeepSeek Flash",
            "resultado": resultado,
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_FLASH,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_FLASH,
        })
    except BadRequestError as error:
        print(f"\nDeepSeek Flash no soporta imágenes: {error}")
        resultados.append({
            "etiqueta": "DeepSeek Flash",
            "resultado": entrada_fallo(modelo_flash, "No soporta visión"),
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_FLASH,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_FLASH,
        })
    except Exception as error:
        print(f"\nError consultando DeepSeek Flash: {error}")
        resultados.append({
            "etiqueta": "DeepSeek Flash",
            "resultado": entrada_fallo(modelo_flash, "Error"),
            "precio_entrada": PRECIO_ENTRADA_DEEPSEEK_FLASH,
            "precio_salida": PRECIO_SALIDA_DEEPSEEK_FLASH,
        })

    # Tabla final
    print("\n" + "=" * 72)
    print("TABLA COMPARATIVA")
    print("=" * 72)
    print(generar_tabla(resultados))


if __name__ == "__main__":
    main()

