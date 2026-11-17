# test_cliente.py

**Ubicación:** [`test_cliente.py`](../../test_cliente.py) · espejo en [`src/test_cliente.py`](../../src/test_cliente.py)

## Qué hace

Es la suite automatizada del cliente modular ([`cliente.py`](cliente.md)). Usa **pytest** con `unittest.mock` y **nunca** llama a la API real: reemplaza `requests.post`, `time.sleep` y las funciones del proyecto por dobles de prueba, así que no consume cuota ni necesita red.

Hoy son **17 funciones** que se recogen como **20 casos**, porque 401/403 y 500/502/503 están parametrizados.

## Cómo se ejecuta

```bash
pytest                          # suite canónica (raíz), 20 casos
pytest test_cliente.py -v       # lo mismo, con el nombre de cada caso
pytest src/test_cliente.py -v   # misma suite sobre src/cliente.py
```

`pytest.ini` fija `testpaths = test_cliente.py`: las dos suites se llaman igual, y si pytest recogiera ambas en la misma corrida fallaría con *import file mismatch* (dos módulos `test_cliente` sin paquete). Por eso `pytest` a secas corre la de la raíz y la de `src/` se pide explícitamente.

## Qué cubre

| Comportamiento esperado | Prueba |
|---|---|
| 401 y 403 salen como `ValueError` | `test_enviar_peticion_credencial_invalida` (2 casos) |
| 429 sale como `TimeoutError` | `test_enviar_peticion_limite_de_uso` |
| 500, 502 y 503 salen como `TimeoutError` | `test_enviar_peticion_error_del_servidor` (3 casos) |
| Un 200 devuelve el JSON tal cual | `test_enviar_peticion_exito` |
| Un `ConnectionError` se clasifica como `TimeoutError` | `test_enviar_peticion_error_de_red_es_timeout` |
| Un 400/404 deja subir el `HTTPError` original | `test_enviar_peticion_otro_4xx_no_esta_clasificado` |
| `con_reintento` reintenta el `TimeoutError` | `test_con_reintento_espera_entre_intentos` |
| `con_reintento` **no** reintenta otro error | `test_con_reintento_no_reintenta_value_error` |
| Al agotar intentos se propaga la excepción original | `test_con_reintento_agota_intentos` |
| Sin error no se duerme | `test_con_reintento_exito_al_primer_intento_no_espera` |
| El backoff respeta `espera_maxima` | `test_con_reintento_respeta_espera_maxima` |
| El costo sale de `totalTokenCount` | `test_registrar_costo_calcula` |
| El costo se acumula en `costo_total_sesion` | `test_registrar_costo_acumula` |
| Sin `usageMetadata` el costo es 0.0 | `test_registrar_costo_sin_metadata` |
| `TimeoutError` agotado → `RuntimeError` | `test_consultar_modelo_convierte_error` |
| `ValueError` se propaga sin cambios | `test_consultar_modelo_propaga_value_error` |
| Camino feliz: texto + costo, sin dormir | `test_consultar_modelo_exito_registra_costo_y_devuelve_texto` |

## Tres decisiones de diseño

1. **`patch` relativo al módulo, no a la librería.** Se parchea `cliente.requests.post` y `cliente.time.sleep` (cómo ve el objeto el módulo bajo prueba). Parchear `requests.post` a secas no tendría efecto: `cliente` ya guardó su propia referencia.
2. **Nunca se compara el jitter.** La espera incluye `random.uniform(0, espera * 0.1)`, así que se verifica *cuántas veces* se llamó a `time.sleep` (`call_count`), o una cota (`<= 1.1`), jamás un valor exacto.
3. **Fixture `autouse` para el estado global.** `costo_total_sesion` es una variable de módulo: la fixture `costo_en_cero` la deja en `0.0` antes y después de cada caso, para que el resultado no dependa del orden de ejecución.

## Cómo agregar una prueba

1. Elige la sección (`enviar_peticion`, `con_reintento`, `registrar_costo`, `consultar_modelo`).
2. Escribe el docstring **explicativo**: qué se verifica, por qué importa y qué se está reemplazando.
3. Si el caso depende de una respuesta HTTP, usa `respuesta_falsa(status_code, datos)`; si depende de un fallo de red, `side_effect=requests.exceptions.ConnectionError(...)`.
4. Replica el cambio en `src/test_cliente.py` (o copia el archivo completo: sólo cambia el docstring inicial).

## Ojo con

- Importar `cliente` carga el `.env`, pero **no** hace ninguna petición: el `__main__` está protegido.
- `respuesta_falsa` devuelve un `Mock`: `raise_for_status()` no lanza nada salvo que se le asigne un `side_effect`, que es justo lo que hace la prueba del 400.
- Las aserciones de costo usan `pytest.approx` porque son `float`.
- La suite no cubre `python cliente.py` de punta a punta (eso sería una prueba de integración con cuota real).

Atte.-</br>
_Jorge Cárdenas Yañez_
