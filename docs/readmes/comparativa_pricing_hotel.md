# comparativa_pricing_hotel.py

**Ubicación:** [`src/comparativa_pricing_hotel.py`](../../src/comparativa_pricing_hotel.py)

## Qué hace

Compara tres modelos con el mismo prompt de texto (precio de una habitación single en el Hotel Amaru): `MODELO 'GEMINI'`, DeepSeek PRO y DeepSeek Flash. Mide respuesta, tokens, costo y latencia, y arma una tabla en Markdown.

## Uso

```bash
python src/comparativa_pricing_hotel.py
```

## Qué necesitas

En el fichero `.env`:

- `GEMINI_API_KEY` y `MODELO`, para Gemini.
- `DEEPSEEK_API_KEY`.
- `modelo_DS_Pro` y `modelo_DS_Flash` (si no están, se usan `deepseek-v4-pro` y `deepseek-flash`).

## Qué hace por dentro

1.- Consulta Gemini con `armar_peticion` + `enviar_peticion`.
2.- Consulta DeepSeek con el SDK de OpenAI (`base_url="https://api.deepseek.com"`).
3.- Normaliza el `usage` de DeepSeek al formato `usageMetadata`, para reutilizar `calcular_costo`.
4.- Si un modelo falla, la tabla muestra su estado ("Error") en vez de cortar la comparación.

## Ojo con

- Cada ejecución son 3 consultas reales; con la cuota justa, Gemini puede responder 429 y la fila queda en "Error".
- El prompt está escrito dentro del script (`main`), no viene del banco de prompts.
- `load_dotenv()` se llama sin ruta, así que conviene ejecutarlo desde la raíz del proyecto.
- Los precios están escritos a mano (`PRECIO_*`); si el proveedor los cambia, la tabla queda desactualizada.



Atte.-</br>
_Jorge Cárdenas Yañez_