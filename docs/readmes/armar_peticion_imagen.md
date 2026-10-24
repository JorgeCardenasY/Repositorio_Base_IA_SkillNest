# armar_peticion_imagen.py

**Ubicación:** [`src/armar_peticion_imagen.py`](../../src/armar_peticion_imagen.py)

## Qué hace

Arma la petición **multimodal** para Gemini: la pregunta más la imagen en base64, dentro de `inlineData`.

Se escribe a razón de separar las dos responsabilidades de mencionadas en `armar_peticion.py`: el texto sigue en su fichero y la imagen se queda acá, durante la actividad a cerca de la toma de decisión respecto de la arquitectura, y por curiosidad técnica :).

## Uso

```python
from armar_peticion_imagen import armar_peticion_imagen

url, body = armar_peticion_imagen(pregunta, imagen_base64)
```

## Qué recibe y qué devuelve

- `pregunta`: el texto que acompaña a la imagen.
- `imagen_base64` (opcional): la imagen ya codificada. Si no viene, la petición queda sólo con texto.
- `mime_type` (opcional): por defecto `"image/png"`.

Devuelve `(url, body)`.

## Ojo con

- Hoy **no** manda `systemInstruction` ni `responseSchema`: es una petición simple de texto + imagen.
- El `mime_type` por defecto es PNG, aunque las imágenes de `imgs/` son `.jpg`. Si Gemini se queja del formato, hay que pasar el tipo real.
- Lo usa `src/comparativa_pricing_img.py`; el resto del proyecto usa `armar_peticion.py`.



Atte.-</br>
_Jorge Cárdenas Yañez_