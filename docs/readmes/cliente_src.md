# src/cliente.py

**Ubicación:** [`src/cliente.py`](../../src/cliente.py) · espejo de [`cliente.py`](../../cliente.py) ([ficha del original](cliente.md))

## Qué hace

Es el **mismo cliente modular** que `cliente.py` de la raíz (envío, reintentos, costo y consulta), pero colocado junto al resto del código fuente para que se pueda importar con un import plano desde cualquier script de `src/`.

Las cuatro funciones (`enviar_peticion`, `con_reintento`, `registrar_costo`, `consultar_modelo`) y su clasificación de errores están explicadas en la [ficha del original](cliente.md); aquí sólo se anotan las diferencias.

## Diferencias con `cliente.py` (raíz)

| Aspecto | Raíz | `src/` |
|---|---|---|
| Imports de helpers | `from src.armar_peticion import armar_peticion` | `from armar_peticion import armar_peticion` |
| `.env` | `Path(__file__).parent / ".env"` | `Path(__file__).parents[1] / ".env"` |
| Comando | `python cliente.py` | `python src/cliente.py` |
| Suite | `pytest test_cliente.py` | `pytest src/test_cliente.py` |

Todo lo demás es idéntico, a propósito: así las dos suites son la misma copia y cualquier cambio se puede replicar sin pensar.

## Uso

```bash
python src/cliente.py
```

```python
# con src/ en sys.path (p. ej. ejecutando desde src/ o con PYTHONPATH=src)
from cliente import consultar_modelo

print(consultar_modelo("¿Cuál es la capital de Chile?"))
```

## Ojo con

- Los imports son **planos**: el módulo espera que `src/` esté en `sys.path` (es la convención de todos los ficheros de esa carpeta). Al ejecutarlo con `python src/cliente.py` eso ocurre solo; al importarlo desde otro sitio hay que añadirlo (`PYTHONPATH=src`).
- Si se ejecuta pytest desde la raíz con la suite completa, `sys.modules["cliente"]` puede apuntar a este módulo o al de la raíz: ambos se comportan igual, pero conviene correr una suite a la vez (`pytest` corre la de la raíz; `pytest src/test_cliente.py` corre ésta).
- Cualquier arreglo hecho en `cliente.py` hay que replicarlo aquí (y al revés).

## Cómo verificarlo

```bash
pytest src/test_cliente.py -v   # 20 casos, sin llamadas reales
```

Atte.-</br>
_Jorge Cárdenas Yañez_
