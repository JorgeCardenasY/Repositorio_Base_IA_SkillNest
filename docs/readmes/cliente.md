# cliente.py

**Ubicación:** [`cliente.py`](../../cliente.py)

## Qué hace

Guarda la función `con_reintento`, pensada para ejecutar otra función y volver a intentarlo si falla por tiempo de espera.

## Uso

```python
from cliente import con_reintento

resultado = con_reintento(
    lambda: enviar_peticion(url, body),
    intentos=3,
    espera_segundos=2,
)
```

## Qué recibe y qué devuelve

- `funcion`: la función que se quiere ejecutar, sin argumentos.
- `intentos`: cuántas veces se intenta (por defecto 3).
- `espera_segundos`: la pausa entre intentos (por defecto 2).

Devuelve lo que devuelva `funcion()` en el primer intento exitoso.

## Ojo con

- Sólo atrapa `TimeoutError`. Hoy `enviar_peticion` lanza `RuntimeError`, así que un 429 o un 503 **no** se reintenta acá: el error sube de inmediato.
- Si el ciclo termina sin retorno, la función devuelve `None` y no avisa.
- Es un script en desarrollo, por lo que quedaron imports y comentarios de borrador (`extraer_texto` no se usa).



Atte.-</br>
_Jorge Cárdenas Yañez_