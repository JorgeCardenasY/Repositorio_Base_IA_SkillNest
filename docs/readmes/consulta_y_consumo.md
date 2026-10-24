# consulta_y_consumo.py

**Ubicación:** [`src/consulta_y_consumo.py`](../../src/consulta_y_consumo.py)

## Qué hace

Reúne las funciones de bajo nivel que usan casi todos los scripts: enviar la petición, sacar el texto y calcular el costo.

## Qué ofrece

- `enviar_peticion(url, body)`: hace el POST, revisa el estado HTTP y devuelve el JSON. Si algo falla, lanza `RuntimeError` con un mensaje entendible.
- `extraer_texto(datos)`: saca `candidates[0].content.parts[0].text`.
- `calcular_costo(datos, precio_entrada, precio_salida)`: multiplica tokens por precio y suma los tokens de razonamiento (`thoughtsTokenCount`) a la salida. Si no hay metadata, devuelve `0.0`.
- `obtener_dato_de_prueba(pregunta)`: ejemplo mínimo que arma, envía y devuelve el texto.

## Uso

```python
from consulta_y_consumo import enviar_peticion, extraer_texto

datos = enviar_peticion(url, body)
print(extraer_texto(datos))
```

## Ojo con

- `requests.post` no lleva `timeout`: si el servicio no responde, la llamada puede quedar colgada.
- El mensaje de error de `enviar_peticion` incluye la URL completa, y la URL lleva la key.
- `obtener_dato_de_prueba` importa `armar_peticion` dentro de la función, para no crear un ciclo de imports.
- Al correrlo solo (`python src/consulta_y_consumo.py`) hace una consulta de prueba sobre "fundion DAX..." (el typo está en el código).



Atte.-</br>
_Jorge Cárdenas Yañez_