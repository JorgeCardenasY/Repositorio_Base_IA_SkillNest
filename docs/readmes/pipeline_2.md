# pipeline_2.py

**Ubicación:** [`src/pipeline_2.py`](../../src/pipeline_2.py)

## Qué hace

Es una variante de [`pipeline.py`](pipeline.md) que añade una medida de **coincidencia entre dos textos**. Reutiliza las mismas funciones de limpieza y tokenización, y al final compara las palabras de una `referencia` con las de una `respuesta`.

No usa Gemini, no lee el `.env` y no gasta cuota.

## Uso

```bash
python src/pipeline_2.py
```

Salida esperada:

```
Coincidencia: 100%
```

Con las frases de ejemplo (`El perro persiguió al gato.` frente a `El gato persiguió al perro.`) las dos usan las mismas cinco palabras, por eso el resultado es 100 %.

## Cómo calcula la coincidencia

1. Procesa `referencia` y `respuesta` con `procesar_texto` (limpiar + tokenizar).
2. Convierte cada lista en un conjunto con `set(...)`.
3. Cuenta las palabras comunes con `&` (intersección).
4. Divide entre el número de palabras distintas de la **referencia**.
5. Si la referencia queda vacía, devuelve `0.0` para evitar dividir entre cero.
6. Muestra el resultado con `f"{proporcion:.0%}"`, que redondea a 0 decimales.

## Ojo con

- **Imprime al importar:** todo el bloque de comparación está a nivel de módulo, sin `if __name__ == "__main__"`. Un `import pipeline_2` imprime `Coincidencia: ...`.
- **Código muerto:** la demostración original quedó dentro de un string de tres comillas (líneas 30-42) y no se ejecuta. La variable `texto` de la línea 29 tampoco se usa.
- **Duplica `pipeline.py`:** las cuatro funciones están copiadas. Si cambias la limpieza o la tokenización, hay que repetir el cambio en los dos ficheros (o importar desde `pipeline`).
- **La medida no es simétrica:** divide solo por las palabras de la referencia (tipo *recall*), no por la unión. Cambiar el orden de los textos cambia el porcentaje. No es «% de similitud» en sentido estricto.
- El porcentaje se redondea a 0 decimales, así que puede mostrar `100%` aunque no coincidan todas las palabras.

Atte.-</br>
_Jorge Cárdenas Yañez_
