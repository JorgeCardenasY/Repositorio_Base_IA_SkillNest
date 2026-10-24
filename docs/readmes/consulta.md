# consulta.py

**Ubicación:** [`src/consulta.py`](../../src/consulta.py)

## Qué hace

Es el ejemplo base del flujo completo: hace **una** pregunta a Gemini y guarda la respuesta ordenada en un diccionario `{clave: valor}`.

## Uso

```bash
python src/consulta.py
```

## Qué hace por dentro

1.- Prepara la petición con `armar_peticion(PREGUNTA, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)`.
2.- La envía con `enviar_peticion`.
3.- Saca el texto con `extraer_texto`.
4.- Lo convierte a diccionario con `parsear_respuesta_json`.
5.- Muestra la respuesta tal cual y después campo por campo.

## Qué devuelve

`main()` devuelve el diccionario (`categoria`, `confianza`, `explicacion`), aunque al correrlo como script el resultado sólo se imprime.

## Ojo con

- La pregunta está fija en `PREGUNTA` (precio del petróleo en Chile); para probar otra cosa hay que editarla.
- Los campos esperados están en `CLAVES_ESPERADAS`; si el modelo se salta uno, salta `ValueError` y se muestra el aviso del final.
- Sirve de modelo para los demás scripts: mismo orden (armar -> enviar -> extraer -> parsear).



Atte.-</br>
_Jorge Cárdenas Yañez_