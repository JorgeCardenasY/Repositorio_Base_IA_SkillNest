# parsear_respuesta.py

**Ubicación:** [`src/parsear_respuesta.py`](../../src/parsear_respuesta.py)

## Qué hace

Convierte el texto que devuelve el modelo en un diccionario de Python. Así que podemos decir que le quita  o filtra la _envoltura de bloque de código_ con que a veces llega la respuesta.

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
- `claves_esperadas` (opcional): los campos que deben existir. Si no se le entregan, se validan `categoria` y `confianza`.

Con todo, devuelve el diccionario ya limpio.

## Ojo con

- Si el texto no es JSON válido, lanza `ValueError("La respuesta del modelo no es JSON válido.")`.
- Si falta una clave, lanza `ValueError("La respuesta no tiene la estructura esperada.")`.
- No valida tipos ni valores: sólo que las claves existan.
- A diferencia de lo mencionado en clases, se desarrolló en un fichero separado.


Atte.-</br>
_Jorge Cárdenas Yañez_