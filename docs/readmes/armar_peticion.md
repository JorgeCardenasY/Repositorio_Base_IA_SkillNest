# armar_peticion.py

**Ubicación:** [`src/armar_peticion.py`](../../src/armar_peticion.py)

## Qué hace

Arma la petición de **texto** para Gemini: devuelve la URL con la API key y el `body` con la pregunta. Si se le pasan instrucciones de sistema o un esquema, los agrega.

Es el fichero que usan todas las consultas de texto: `consulta.py`, `consistencia.py`, `consumir_gemini.py` y `comparativa_pricing_hotel.py`.

## Uso

```python
from armar_peticion import armar_peticion

# Sólo la pregunta
url, body = armar_peticion("¿Cuál es la capital de Chile?")

# Con rol y esquema JSON
url, body = armar_peticion(PREGUNTA, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)
```

## Qué recibe y qué devuelve

- `pregunta_usuario`: el texto que se le manda al modelo.
- `system_instruction` (opcional): el rol o las reglas. Si viene vacío, no se envía `systemInstruction`.
- `response_schema` (opcional): el esquema JSON. Si viene, se agrega `generationConfig` con `responseMimeType: application/json`.

Devuelve una tupla `(url, body)`, lista para `enviar_peticion`.

## Ojo con

- Lee `GEMINI_API_KEY` y `MODELO` desde el `.env` de la raíz, con ruta absoluta, así funciona desde cualquier carpeta.
- No maneja imágenes: para eso está `armar_peticion_imagen.py`.
- La key viaja en la URL (`?key=...`); por eso los errores no deberían mostrar la URL completa.



Atte.-</br>
_Jorge Cárdenas Yañez_