# consistencia.py

**Ubicación:** [`src/consistencia.py`](../../src/consistencia.py)

## Qué hace

Mide la consistencia del modelo: repite cada prompt del banco `prompts/banco.py` 3 veces y cuenta cuántas respuestas llegan con la estructura esperada. Al final deja el resumen en `prompts/registro.json`.

## Uso

```bash
python src/consistencia.py
```

## Qué hace por dentro

1.- Recorre `BANCO_DE_PROMPT` (hoy son 2 hoteles). </br>
2.- Por cada prompt arma la petición con `system_instruction` y `response_schema`.</br>
3.- Intenta 3 veces, valida con `parsear_respuesta_json` y cuenta los aciertos.</br>
4.- Escribe el avance en `prompts/registro.json`, con la forma `{"HotelAmaru": {"exitos": 3, "intentos": 3}, ...}`.</br>

## Ojo con

- Son 6 consultas reales por corrida (2 prompts x 3 intentos). Si la cuota está justa, el 429 corta todo el ciclo.
- No tiene constructor `__main__`: **importar** este fichero dispara las peticiones. Por ello, se debe ejecutar directamente, no importarlo.
- El registro es un artefacto de salida; hoy queda como fichero sin versionar.
- Si se agrega un prompt al banco, el registro parte de cero en la siguiente corrida.



Atte.-</br>
_Jorge Cárdenas Yañez_