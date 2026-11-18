# test_cliente.py

**Ubicación:** [`src/test_cliente.py`](../../src/test_cliente.py)

## ¿Qué es?

Un archivo con pruebas automáticas. Revisa que el cliente de Gemini ([`src/cliente.py`](../../src/cliente.py)) haga lo correcto.

Las pruebas **nunca** llaman a la API real: reemplazan la red y las esperas por "dobles" (mocks). Por eso no gastan cuota y funcionan sin internet.

Hoy son **17 funciones** que se ejecutan como **20 casos**, porque dos de ellas se repiten con varios códigos de error.

## ¿Qué necesitas?

- Python.
- `pytest` (ya está en `requirements.txt`).
- No hace falta una API key real ni conexión.

## Cómo se ejecuta

```bash
pytest                          # todos los casos
pytest src/test_cliente.py -v   # igual, pero con el nombre de cada caso
```

Deberías ver: **20 passed**.

El archivo `pytest.ini` ya apunta a esta suite (`testpaths = src/test_cliente.py`), por eso `pytest` a secas funciona.

## ¿Qué revisa?

### 1. Hablar con el servidor (`enviar_peticion`) — 9 casos

- Clave mala (401 o 403) → error `ValueError`.
- Demasiadas peticiones (429) → `TimeoutError`.
- Fallo del servidor (500, 502 o 503) → `TimeoutError`.
- Todo bien (200) → devuelve los datos tal cual.
- Se cae la red → `TimeoutError`.
- Otro error (400 o 404) → se deja pasar el error original.

### 2. Reintentar (`con_reintento`) — 5 casos

- Si hay `TimeoutError`, espera y vuelve a intentarlo.
- Si el error es distinto, **no** reintenta.
- Cuando se acaban los intentos, devuelve el último error.
- Si sale bien a la primera, no espera nada.
- La espera nunca supera `espera_maxima`.

### 3. Calcular el costo (`registrar_costo`) — 3 casos

- Calcula el costo con `totalTokenCount`.
- Suma el costo al total de la sesión (`costo_total_sesion`).
- Si no vienen datos de uso, el costo es `0.0`.

### 4. Consultar el modelo (`consultar_modelo`) — 3 casos

- Si se agotan los reintentos → `RuntimeError`.
- Si hay un `ValueError`, sube sin cambios.
- Camino feliz: devuelve el texto y suma el costo.

## Cuatro palabras que conviene saber

- **Prueba (test):** función que empieza por `test_`. Si no empieza así, pytest no la ejecuta.
- **Mock:** un doble que ocupa el lugar de algo real (por ejemplo, la red).
- **Fixture:** función que prepara algo antes de las pruebas. Con `autouse=True` se ejecuta sola en todas.
- **Parametrizar:** repetir la misma prueba con varios datos.

## ¿Cómo se ve una prueba?

```python
def test_enviar_peticion_exito():
    """Un 200 devuelve el JSON tal cual."""
    datos = {"candidates": [{"content": {"parts": [{"text": "Santiago"}]}}]}
    with patch("cliente.requests.post", return_value=respuesta_falsa(200, datos)):
        resultado = enviar_peticion({"contents": []})

    assert resultado is datos
```

Se cambia `requests.post` por un mock, se llama a la función real y se compara el resultado.

## Reglas de oro

1. No llamar nunca a la API real: siempre `patch("cliente.requests.post", ...)`.
2. No comparar tiempos exactos: la espera incluye azar (`random.uniform`).
3. No poner `@pytest.fixture` en una función `test_`: dejaría de ser prueba.
4. Cada prueba debe pasar sola y en cualquier orden.

## Si algo falla

- `ModuleNotFoundError: cliente` → ejecuta desde la raíz del repositorio (o usa `pytest` a secas).
- Falla un caso de 401/403 → revisa que se lance `ValueError`.
- Falla un caso de 429 o 5xx → revisa que se lance `TimeoutError`.
- Un test "no se ejecuta" → comprueba que su nombre empiece por `test_`.

## Para saber más

- Código: [`src/test_cliente.py`](../../src/test_cliente.py)
- Cliente que se prueba: [`src/cliente.py`](../../src/cliente.py) · ficha: [cliente.md](cliente.md)

Atte.-</br>
_Jorge Cárdenas Yañez_
