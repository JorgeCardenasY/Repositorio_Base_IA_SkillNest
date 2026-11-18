# src/cliente.py

**Ubicación:** [`src/cliente.py`](../../src/cliente.py)

## Qué hace

Es el cliente modular del proyecto: reúne en un solo fichero las cuatro piezas que antes estaban repartidas entre `cliente_api.py`, `cliente_reintento.py` y `consulta_y_consumo.py`. Ya **no** es un borrador: compila, se puede importar sin efectos secundarios y tiene pruebas automatizadas ([ficha de la suite](test_cliente.md)).

## Qué ofrece

| Función | Qué hace |
|---|---|
| `enviar_peticion(cuerpo)` | Hace el `POST` a Gemini y devuelve el JSON **tal cual**. Clasifica los fallos antes de devolver nada. |
| `con_reintento(funcion, intentos=3, espera_base=2, espera_maxima=30)` | Ejecuta `funcion()` y reintenta sólo si falla con `TimeoutError`, con backoff exponencial y jitter. |
| `registrar_costo(respuesta)` | Lee `usageMetadata.totalTokenCount`, calcula el costo de la operación y lo suma a `costo_total_sesion`. |
| `consultar_modelo(pregunta, system_instruction="")` | Orquesta el flujo completo: armar → enviar con reintentos → registrar costo → devolver el texto. |

## Uso

```bash
python src/cliente.py
```

```python
# con src/ en sys.path (p. ej. PYTHONPATH=src)
from cliente import consultar_modelo

print(consultar_modelo("¿Cuál es la capital de Chile?"))
```

## Clasificación de errores

| Respuesta del proveedor | Excepción que sale | ¿Se reintenta? |
|---|---|---|
| 200 | — (devuelve el JSON) | — |
| **401 / 403** (credencial inválida) | `ValueError` | No |
| **429** (límite de uso) | `TimeoutError` | Sí, hasta 3 intentos |
| **5xx** (fallo del servidor) | `TimeoutError` | Sí, hasta 3 intentos |
| Timeout o `ConnectionError` de red | `TimeoutError` | Sí, hasta 3 intentos |
| Otros 4xx (400, 404…) | `requests.HTTPError` | No |

`consultar_modelo` convierte el `TimeoutError` agotado en `RuntimeError("El servicio no respondió tras varios intentos…")`; el `ValueError` y el `HTTPError` suben **sin cambios**.

## Cuánto se espera entre intentos

`min(espera_base * 2 ** (intento - 1), espera_maxima)` segundos **más** un jitter aleatorio de hasta 10 %. Con los valores por defecto: ~2 s, luego ~4 s, y el tope de 30 s para sesiones con muchos reintentos. Por eso las pruebas verifican *cuántas veces* se llamó a `time.sleep`, nunca el valor exacto.

## Ojo con

- `URL`, `headers` y `MODELO` se calculan **al importar**: si cambias el `.env`, hay que reiniciar el proceso (o volver a importar).
- La `GEMINI_API_KEY` viaja en la URL (`?key=…`). Es el mismo esquema del borrador original; si esto pasara a producción conviene moverla a la cabecera `x-goog-api-key`, como hace `consulta_y_consumo.py`. Este módulo nunca imprime la URL en sus mensajes de error.
- `COSTO_POR_1000_TOKENS = 0.002` es un precio **referencial** para comparar sesiones, no la tarifa oficial.
- `costo_total_sesion` es estado global del módulo: si lo pruebas, reinícialo entre casos (la suite lo hace con una fixture `autouse`).
- `con_reintento` con `intentos=0` no ejecuta nada y devuelve `None`: es una entrada sin validar, aunque el valor por defecto (3) lo evita.
- Los imports son **planos**: el módulo espera que `src/` esté en `sys.path` (es la convención de todos los ficheros de esa carpeta). Al ejecutarlo con `python src/cliente.py` eso ocurre solo; al importarlo desde otro sitio hay que añadirlo (`PYTHONPATH=src`), como hace `app.py`.
- Las pruebas reemplazan todo con `patch("cliente.requests.post")` y `patch("cliente.time.sleep")`: no gastan cuota.

## Cómo verificarlo

```bash
pytest src/test_cliente.py -v     # 20 casos, sin llamadas reales
```

Atte.-</br>
_Jorge Cárdenas Yañez_
