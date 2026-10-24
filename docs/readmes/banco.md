# banco.py

**Ubicación:** [`prompts/banco.py`](../../prompts/banco.py)

## Qué hace

Es el banco de prompts de prueba. Guarda la lista `BANCO_DE_PROMPT` con dos fichas de hotel: Hotel Amaru y Hotel Spa Las Taguas.

Cada ficha tiene:

1.- `nombre`: cómo se identifica el prompt en el registro.
2.- `system_instruction`: el rol que se le da al modelo.
3.- `ejemplo_usuario`: la pregunta de ejemplo.
4.- `claves_esperadas`: los campos que deben venir en la respuesta.
5.- `response_schema`: la plantilla JSON que se le pasa a Gemini.

## Uso

```python
from prompts.banco import BANCO_DE_PROMPT

for prompt in BANCO_DE_PROMPT:
    print(prompt["nombre"])
```

## Precauciones:

- Es un fichero de datos, no un script: no se ejecuta solo.
- Lo consume `src/consistencia.py`; por cada ficha se hacen 3 consultas (los 3 intentos).
- Las claves del esquema llevan espacios a propósito ("Distancia del Morro de Arica"). Gemini las acepta tal cual, pero hay que respetarlas también en `claves_esperadas`.




Atte.-</br>
_Jorge Cárdenas Yañez_