# cliente_reintento_rate_limit.py

**Ubicación:** [`src/cliente_reintento_rate_limit.py`](../../src/cliente_reintento_rate_limit.py)

## Qué hace

Lanza **10 consultas seguidas** a Gemini usando el cliente del proyecto (`armar_peticion` + `consulta_y_consumo.enviar_peticion`) y envuelve cada envío en `con_reintento`, una política de reintentos con **backoff exponencial y jitter**. Sirve para provocar el HTTP 429 (límite de peticiones) y ver en pantalla cómo el script espera y vuelve a intentar en vez de abortar.

## Uso

```bash
python src/cliente_reintento_rate_limit.py
```

Cada ejecución hace hasta **10 consultas reales** y, si el proveedor responde 429/5xx, hasta **3 envíos por consulta** (30 peticiones en el peor caso). Ojo con la cuota gratuita.

## Qué hace por dentro

1.- Arma la petición con `armar_peticion(pregunta, system_instruction)`, que lee `GEMINI_API_KEY` y `MODELO` del `.env` y devuelve `(url, body)`.</br>
2.- La envía con `con_reintento(lambda: enviar_peticion(url, body))`.</br>
3.- Registra el costo con `registrar_costo` a partir de `usageMetadata.totalTokenCount`.</br>
4.- Extrae el texto con `extraer_texto`.</br>
5.- Repite 10 veces y, al final, imprime el costo acumulado de la sesión.

## Política de reintentos

| Excepción que sale de `enviar_peticion` | ¿Se reintenta? | Qué hace el script |
|---|---|---|
| `TimeoutError` (timeout de red, `ConnectionError`, **429**, **5xx**) | Sí, hasta 3 intentos | Espera `min(2 * 2 ** (intento - 1), 30)` s más un *jitter* de hasta 10 % y reintenta. Si se agotan, `consultar_modelo` lanza `RuntimeError`. |
| `ValueError` (**401/403**) | No | Sube tal cual; el `__main__` la informa como «falló definitivamente», sin traceback. |
| `requests.HTTPError` (**400/404**, p. ej. `MODELO` inexistente) | No | Se convierte en `RuntimeError("Error definitivo del proveedor: …")`. |
| `RuntimeError` de `extraer_texto` (respuesta sin `candidates`) | No | Se informa como fallo definitivo de esa consulta. |

## Ojo con

- **`Retry-After`**: `enviar_peticion` lo anuncia en el mensaje del 429 («Reintentar en 30 s»), pero el backoff sólo espera 2 s y luego 4 s. En cuota gratuita lo normal es recibir otro 429 y terminar en `RuntimeError`; el script existe justamente para verlo en vivo.
- `MODELO` (en mayúsculas) es la variable que lee `armar_peticion.py`; el `.env` de este repositorio apunta a `gemini-3.6-flash`. Cambiarla cambia el modelo sin tocar el código.
- `COSTO_POR_1000_TOKENS = 0.002` es un precio **referencial** para comparar sesiones, no la tarifa oficial.
- Al importarlo desde otro script hay que tener `src/` en `sys.path`: los módulos de `src/` usan imports planos.
- Es casi el mismo código que `cliente_reintento.py`; la diferencia es el bucle de 10 consultas y el costo acumulado de la sesión.

Atte.-</br>
_Jorge Cárdenas Yañez_
