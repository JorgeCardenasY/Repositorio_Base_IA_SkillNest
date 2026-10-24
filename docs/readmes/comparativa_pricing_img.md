# comparativa_pricing_img.py

**Ubicación:** [`src/comparativa_pricing_img.py`](../../src/comparativa_pricing_img.py)

## Qué hace

Hace la misma comparativa, pero con imagen: le pasa una foto de patente a los tres modelos y compara la placa extraída, tokens, costo y latencia.

## Uso

```bash
python src/comparativa_pricing_img.py imgs/patente1.jpg
```

Si no se pasa ruta, intenta con `placa.png`, que no está en el repositorio.

## Qué necesitas

- Las mismas variables del `.env` que la comparativa de texto.
- Una imagen; las de prueba están en `imgs/patente0.jpg` ... `imgs/patente5.jpg`.

## Qué hace por dentro

1.- `codificar_imagen` lee el fichero y lo pasa a base64.
2.- Gemini recibe la imagen con `armar_peticion_imagen` (`inlineData`).
3.- DeepSeek la recibe como `image_url` con `data:image/png;base64,...`.
4.- Si DeepSeek rechaza la imagen (`BadRequestError`), la fila queda como "No soporta visión".

## Ojo con

- La imagen se declara siempre como `image/png`, aunque los ficheros de `imgs/` sean `.jpg`.
- El docstring todavía dice `python src/comparativa_pricing.py`; el nombre real del fichero es `comparativa_pricing_img.py`.
- Cada corrida son 3 consultas, y la imagen pesa en los tokens de entrada.


Atte.-</br>
_Jorge Cárdenas Yañez_