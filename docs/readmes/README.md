# README de los ficheros .py

Este índice lleva a la explicación de cada fichero Python del repositorio. La idea es la misma en todos: qué hace, cómo se usa y con qué hay que tener cuidado.

## Raíz

- [`app.py`](app.md): prueba inicial con `cowsay`.
- [`cliente.py`](cliente.md): helper de reintentos, en estado de borrador.

## src/

- [`armar_peticion.py`](armar_peticion.md): arma la petición de texto.
- [`armar_peticion_imagen.py`](armar_peticion_imagen.md): arma la petición con imagen.
- [`comparativa_pricing_hotel.py`](comparativa_pricing_hotel.md): comparativa de texto entre modelos.
- [`comparativa_pricing_img.py`](comparativa_pricing_img.md): comparativa con imagen de patente.
- [`consistencia.py`](consistencia.md): 3 intentos por prompt y registro de resultados.
- [`consulta.py`](consulta.md): flujo completo de una consulta.
- [`consulta_y_consumo.py`](consulta_y_consumo.md): envío, extracción de texto y costo.
- [`consumir_gemini.py`](consumir_gemini.md): latencia y costo de 4 consultas.
- [`parsear_respuesta.py`](parsear_respuesta.md): texto del modelo -> diccionario.

## prompts/

- [`banco.py`](banco.md): banco de prompts de prueba.

## Lectura sugerida

En orden a comprender de manera lógica el repositorio, tenga a bien aceptar la sugerencia de abordar el repositorio en este ŕoden: `consulta_y_consumo.md` -> `armar_peticion.md` -> `consulta.md`. Con esos tres se entiende el flujo base; el resto son variantes (imagen, comparativas, consistencia).
