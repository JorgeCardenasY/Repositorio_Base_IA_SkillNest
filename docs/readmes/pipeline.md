# pipeline.py

**Ubicación:** [`src/pipeline.py`](../../src/pipeline.py)

## Qué hace

Es un mini *pipeline* de texto: recibe una frase, la normaliza, la corta en palabras y puede contar cuántas veces aparece cada una. No usa la API de Gemini, no lee el `.env` y no gasta cuota: sirve para preparar texto antes de compararlo o analizarlo.

## Uso

```bash
python src/pipeline.py
```

Salida esperada (con el texto de ejemplo que trae el fichero):

```
Conteo: Counter({'santiago': 2, 'es': 2, 'la': 1, 'capital': 1, 'de': 1, 'chile': 1, 'horrible': 1})
Texto limpio: ['santiago', 'es', 'la', 'capital', 'de', 'chile', 'santiago', 'es', 'horrible']
```

> La etiqueta `Texto limpio:` es engañosa: imprime la **lista de tokens**, no la cadena limpia.

## Qué hace por dentro

| Función | Entrada | Salida | Qué hace |
|---|---|---|---|
| `limpiar_texto(texto)` | `str` | `str` | Pasa a minúsculas, quita la puntuación, junta los espacios repetidos y recorta los extremos. Lanza `TypeError` si no recibe `str`. |
| `tokenizar(texto_limpio)` | `str` | `list[str]` | Corta por espacios con `.split()`. |
| `vectorizar(tokens)` | `list[str]` | `Counter` | Cuenta cuántas veces aparece cada palabra. |
| `procesar_texto(texto)` | `str` | `list[str]` | Atajo: `limpiar_texto` + `tokenizar`. **No** cuenta palabras. |

Ejemplo verificado:

```python
import sys
sys.path.insert(0, "src")
from pipeline import procesar_texto

print(procesar_texto("¡Hola, Mundo!  Programación en PYTHON."))
# ['hola', 'mundo', 'programación', 'en', 'python']
```

El `__main__` solo ejecuta la demostración; importar el módulo no imprime nada ni tiene efectos secundarios.

## Ojo con

- **No quita tildes:** `programación` y `programacion` son tokens distintos. Si necesitas compararlos, normaliza aparte (por ejemplo, con `unicodedata`).
- **No quita *stopwords*:** palabras como `es`, `la` o `de` se cuentan igual que las demás.
- La limpieza usa `re.sub(r"[^\w\s]", "", texto)`; en Python 3 `\w` incluye letras acentuadas, así que `programación` sobrevive intacta.
- `procesar_texto` devuelve **tokens**, no un `Counter`: si quieres el conteo, encadena `vectorizar(procesar_texto(texto))`.
- `Counter` se imprime con su propia sintaxis (`Counter({...})`), no como un `dict` normal.

Atte.-</br>
_Jorge Cárdenas Yañez_
