# consulta.py

**Ubicación:** [`src/consulta.py`](../../src/consulta.py)

## Qué hace

Es el ejemplo base del flujo completo: hace **una** pregunta a Gemini y guarda la respuesta ordenada en un diccionario con datos ordenados tipo :`{clave: valor}`.

## Uso

```bash
python src/consulta.py
```

## Qué hace por dentro

1.- Prepara la petición con `armar_peticion(PREGUNTA, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)`.</br>
2.- La envía con `enviar_peticion`.</br>
3.- Saca el texto con `extraer_texto`.</br>
4.- Lo convierte a diccionario con `parsear_respuesta_json`.</br>
5.- Muestra la respuesta tal cual y después campo por campo.</br>
</br>
## Qué devuelve

`main()` devuelve el diccionario con las claves `categoria`, `confianza` y `explicacion`. Es importante señalar que  al correr `python src/consulta.py`, el constructor `__main__` llama a `main()` sin guardar el `return`. De este modo, podemos decir que el resultado es _descartado_, ya que no es _almacenado_ aún. Dicho de otro modo, lo que se imprime en pantalla son los `print` de dentro de `main()` (texto crudo y después campo por campo) ya que el diccionario no se guarda en ningún fichero. Para reutilizarlo hay que importar `main` y capturar su `return`.


## Ojo con

- La pregunta está fija en `PREGUNTA` (precio del petróleo en Chile); para probar otra cosa hay que editarla.
- Los campos esperados están en `CLAVES_ESPERADAS`; si el modelo se salta uno, salta `ValueError` y se muestra el aviso del final.
- Sirve de modelo para los demás scripts: mismo orden (armar -> enviar -> extraer -> parsear).



Atte.-</br>
_Jorge Cárdenas Yañez_