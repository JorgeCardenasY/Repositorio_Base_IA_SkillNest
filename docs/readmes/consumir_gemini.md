# consumir_gemini.py

**Ubicación:** [`src/consumir_gemini.py`](../../src/consumir_gemini.py)

## Qué hace

Mide cuánto demora y cuánto cuesta una consulta. Hace 4 peticiones seguidas con la misma pregunta, promedia la latencia y calcula el costo de la última.

## Uso

```bash
python src/consumir_gemini.py
```

## Qué hace por dentro

1.- Arma con `armar_peticion(pregunta)`, sin rol ni esquema.
2.- Mide con `time.perf_counter()` antes y después de `enviar_peticion`.
3.- Calcula el promedio de los 4 intentos.
4.- Calcula el costo con `calcular_costo`, usando `PRECIO_ENTRADA` y `PRECIO_SALIDA`.

## Ojo con

- Son 4 consultas reales por corrida; sirve para medir latencia, pero gasta cuota.
- Los precios están escritos como constantes ("el valor real de la página de precios"); si cambian, hay que actualizarlos a mano.
- Devuelve el JSON de la última respuesta, no el promedio.



Atte.-</br>
_Jorge Cárdenas Yañez_