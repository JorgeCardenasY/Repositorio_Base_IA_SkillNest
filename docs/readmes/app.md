# app.py

**Ubicación:** [`app.py`](../../app.py)

## Qué hace

Es el punto de entrada del repositorio: hace **una** consulta real a Gemini y muestra la pregunta, la respuesta del modelo y el costo estimado de esa consulta.

No reescribe la conexión desde cero ni agrega dependencias: reutiliza las funciones que ya existen en `src/` (`armar_peticion`, `enviar_peticion`, `extraer_texto` y `calcular_costo`), y toma la API key y el modelo desde el `.env` de la raíz (`GEMINI_API_KEY` y `MODELO`).

## Uso

```bash
# Pregunta por defecto (PREGUNTA_POR_DEFECTO)
python app.py

# Pregunta propia, pasada por la línea de comandos
python app.py "¿Cuál es la capital de Chile y cuántos habitantes tiene?"
```

## Qué hace por dentro

1.- Agrega la carpeta `src/` al `sys.path`, porque los módulos de ahí usan imports _planos_ (`from armar_peticion import armar_peticion`) y no se pueden importar desde la raíz como paquete.</br>
2.- Arma la petición con `armar_peticion(pregunta)`, sin `system_instruction` ni esquema JSON: la respuesta llega como texto libre.</br>
3.- La envía con `enviar_peticion`.</br>
4.- Saca el texto con `extraer_texto`.</br>
5.- Calcula el costo con `calcular_costo`, usando `PRECIO_ENTRADA` y `PRECIO_SALIDA` (los mismos valores de `consumir_gemini.py`).</br>
6.- Imprime pregunta, respuesta y costo estimado en USD.</br>

## Qué recibe y qué devuelve

- Sin argumentos: usa la constante `PREGUNTA_POR_DEFECTO`.
- Con argumentos: une `sys.argv[1:]` con espacios y usa eso como pregunta (conviene escribirla entre comillas).

`main()` devuelve el texto de la respuesta. Al correr `python app.py`, el bloque `__main__` llama a `main()` sin guardar el `return`, así que en pantalla sólo se ve lo que imprimen los `print`. Para reutilizar el texto hay que importar `main` y capturar su `return`.

## Ojo con

- Cada corrida es **1 consulta real**: consume cuota. Si aparece un 429, hay que esperar o cambiar `MODELO` en el `.env`.
- `enviar_peticion` no lleva `timeout` ni reintentos: si el servicio no responde, la llamada puede quedar colgada y no hay segundo intento (para eso está `cliente.py`, aún en borrador).
- Los errores de `enviar_peticion` incluyen la URL con la llave; el `except` de `app.py` corta el mensaje en `?key=` para **no mostrar la API key** en consola.
- El aviso de error se imprime, pero el proceso termina con código 0: si se usa en un script o CI, hay que revisar el texto, no el `exit code`.
- Los precios están como constantes en el propio fichero; si cambian, hay que actualizarlos a mano (igual que en `consumir_gemini.py`).
- Si `MODELO` del `.env` no existe para la key, Gemini responde 404 y aparece "No se pudo completar la consulta...", sin traza de error.
- Ya no usa `cowsay`: la dependencia sigue en `requirements.txt`, pero `app.py` no la importa.



Atte.-</br>
_Jorge Cárdenas Yañez_