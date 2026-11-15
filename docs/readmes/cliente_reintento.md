# cliente_reintento.py

**Ubicación:** [`src/cliente_reintento.py`](../../src/cliente_reintento.py)

## Qué hace

Hace **una** consulta real a Gemini, pero envolviendo el cliente del proyecto (`consulta_y_consumo.enviar_peticion`) en una política de reintentos con **backoff exponencial y jitter**. La diferencia con `consulta.py` es que aquí el envío se repite automáticamente si el fallo es transitorio (timeout, `ConnectionError`, HTTP 429 o HTTP 5xx), y se aborta de inmediato si el error es definitivo, para no gastar cuota.

## Uso

```bash
python src/cliente_reintento.py
```

Cada ejecución consume **1 consulta real**; si el proveedor responde 429/5xx puede llegar hasta **3** (una por intento).

## Qué hace por dentro

1.- Valida que el `.env` traiga `GEMINI_API_KEY` y `MODELO` (`validar_configuracion`).</br>
2.- Arma la petición con `armar_peticion(PREGUNTA, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)`.</br>
3.- La envía con `con_reintento(lambda: enviar_peticion(url, body))`.</br>
4.- Extrae el texto con `extraer_texto` y lo convierte en diccionario con `parsear_respuesta_json`.</br>
5.- Calcula el costo con `calcular_costo` y muestra el texto crudo, los campos, el intento en que se logró y el costo estimado.</br>

## Qué devuelve

- `con_reintento()` devuelve una tupla `(resultado, número_de_intento)`.
- `hacer_consulta()` devuelve un `dict` con las claves `intento`, `texto`, `datos` y `costo`.
- `main()` devuelve `0` si la consulta se completó y `1` si hubo un error controlado; el `if __name__ == "__main__"` lo convierte en código de salida con `raise SystemExit(main())`.

## Política de reintentos

| Excepción que sale de `consulta_y_consumo.enviar_peticion` | ¿Se reintenta? | Motivo |
|---|---|---|
| `TimeoutError` (timeout de red, `ConnectionError`, **429**, **5xx**) | Sí | Es transitorio: esperar y volver a intentar suele resolverlo. |
| `ValueError` (**401/403**) | No | Credencial inválida: reintentar no la arregla y gasta cuota. |
| `requests.HTTPError` (**400/404**) | No | Petición mal formada o `MODELO` inexistente. Se reporta como `RuntimeError`. |
| `ValueError` de `parsear_respuesta_json` | No | El modelo no respetó el esquema JSON; se avisa en `main()`. |

La espera entre intentos es `min(espera_base * 2 ** (intento - 1), espera_maxima)` más un *jitter* de hasta un 10 %, con `ESPERA_BASE = 2.0` y `ESPERA_MAXIMA = 30.0`.

## Ojo con

- `MODELO` (así, en mayúsculas) es la variable que lee `armar_peticion.py`; el `.env` también define `modelo` (minúsculas), que usan las comparativas. Si `MODELO` no existe en Google, la respuesta es 404 y el script lo informa como error definitivo, sin reintentar.
- No importar el módulo desde otro script sin tener `src/` en `sys.path`: es el mismo requisito que `consulta.py`.
- El mock que traía este fichero se eliminó: aquí **siempre** se usa el cliente real. Para probar la política sin gastar cuota, usa una función falsa:

```python
import sys
sys.path.insert(0, "src")
from cliente_reintento import con_reintento

llamadas = {"n": 0}

def falso():
    llamadas["n"] += 1
    if llamadas["n"] < 3:
        raise TimeoutError("429 simulado")
    return "ok"

print(con_reintento(falso, espera_base=0))   # ('ok', 3), sin dormir ni consultar
```

- `cliente.py` de la raíz sigue siendo un **borrador** (imports duplicados y `armar_peticion` con 3 argumentos); la versión de referencia de la política de reintentos es este fichero.

Atte.-</br>
_Jorge Cárdenas Yañez_
