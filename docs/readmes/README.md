# README de los ficheros .py

Este índice lleva a la explicación de cada fichero Python del repositorio. La idea es la misma en todos: qué hace, cómo se usa y con qué hay que tener cuidado.

## Raíz

- [`app.py`](app.md): punto de entrada; una consulta real a Gemini con costo estimado.
- [`cliente.py`](cliente.md): cliente modular (envío, reintentos, costo y consulta) con pruebas propias.
- [`test_cliente.py`](test_cliente.md): suite de 20 casos del cliente, con mocks y sin llamadas reales.

## src/

- [`armar_peticion.py`](armar_peticion.md): arma la petición de texto.
- [`armar_peticion_imagen.py`](armar_peticion_imagen.md): arma la petición con imagen.
- [`cliente.py`](cliente_src.md): espejo del cliente modular, con imports planos.
- [`cliente_reintento.py`](cliente_reintento.md): una consulta con reintentos y backoff exponencial.
- [`cliente_reintento_rate_limit.py`](cliente_reintento_rate_limit.md): 10 consultas seguidas para provocar el 429 y ver el backoff.
- [`comparativa_pricing_hotel.py`](comparativa_pricing_hotel.md): comparativa de texto entre modelos.
- [`comparativa_pricing_img.py`](comparativa_pricing_img.md): comparativa con imagen de patente.
- [`consistencia.py`](consistencia.md): 3 intentos por prompt y registro de resultados.
- [`consulta.py`](consulta.md): flujo completo de una consulta.
- [`consulta_y_consumo.py`](consulta_y_consumo.md): envío, extracción de texto y costo.
- [`consumir_gemini.py`](consumir_gemini.md): latencia y costo de 4 consultas.
- [`parsear_respuesta.py`](parsear_respuesta.md): texto del modelo -> diccionario.
- [`test_cliente.py`](test_cliente.md): la misma suite del cliente, aplicada a `src/cliente.py`.

## prompts/

- [`banco.py`](banco.md): banco de prompts de prueba.

## Lectura sugerida

En orden a comprender de manera lógica el repositorio, tenga a bien aceptar la sugerencia de abordar el repositorio en este ŕoden: `consulta_y_consumo.md` -> `armar_peticion.md` -> `consulta.md`. Con esos tres se entiende el flujo base; el resto son variantes (imagen, comparativas, consistencia).
