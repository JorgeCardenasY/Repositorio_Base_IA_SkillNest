# parsear_respuesta.py

**Ubicación:** [`src/parsear_respuesta.py`](../../src/parsear_respuesta.py)

## Qué hace

Convierte el texto que devuelve el modelo en un diccionario de Python. Antes le quita la envoltura de bloque de código con que a veces llega la respuesta.

## Uso

```python
from parsear_respuesta import parsear_respuesta_json

datos = parsear_respuesta_json(
    texto,
    ["categoria", "confianza", "explicacion"],
)
```

## Qué recibe y qué devuelve

- `texto`: la respuesta cruda del modelo.
- `claves_esperadas` (opcional): los campos que deben existir. Si no se pasan, se validan `categoria` y `confianza`.

Devuelve el diccionario ya limpio.

## Ojo con

- Si el texto no es JSON válido, lanza `ValueError("La respuesta del modelo no es JSON válido.")`.
- Si falta una clave, lanza `ValueError("La respuesta no tiene la estructura esperada.")`.
- No valida tipos ni valores: sólo que las claves existan.


Atte.-</br>
_Jorge Cárdenas Yañez_