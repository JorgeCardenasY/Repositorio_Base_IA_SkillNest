# Límites de la métrica de evaluación

## Qué mide

Cuenta cuántos tokens (palabras normalizadas: minúsculas y sin
puntuación) coinciden entre la referencia y la respuesta, respetando
repeticiones, y con eso calcula `precision` (coincidencias / tokens de
la respuesta), `cobertura` (coincidencias / tokens de la referencia) y
`f1` (media armónica de ambas). No comprueba si el dato es verdadero, ni
si el orden del discurso tiene sentido, ni si la negación es la correcta.

## Modos de falla conocidos

- **Una respuesta correcta y exhaustiva puntúa casi cero si es larga.**
  `precision` divide entre *todos* los tokens de la respuesta. Ejemplo
  de la muestra: "Explícame con detalle qué es una tupla en Python."
  f1 = 0.023 con cobertura 1.0; "Explícame con detalle qué es un
  diccionario en Python." f1 = 0.024. Ambas verificadas como correctas.

- **Un sinónimo cuesta más que un dato omitido.** "¿Qué hace el método
  append() en una lista?" responde "añade" en lugar de "agrega" y
  obtiene f1 = 0.667; "¿En qué año se publicó la primera versión de
  Python?", que omite el dato central de la referencia (la versión
  0.9.0), obtiene 0.600. La métrica castiga la redacción, no la falta de
  contenido.

- **Un detalle extra correcto baja el puntaje.** "¿Quién creó Python?"
  (f1 = 0.824) dice exactamente lo mismo que la referencia más "el
  programador holandés"; esos tres tokens impiden el 1.0.

- **La forma del sí/no define el puntaje más que la respuesta.** "¿Se
  puede modificar una tupla después de crearla en Python?" es correcta y
  directa ("las tuplas son inmutables") y saca 0.182, porque la única
  coincidencia con la referencia es el token "no". "¿Python se compila a
  código máquina antes de ejecutarse?" (0.258) es técnicamente *más*
  precisa que la referencia: distingue bytecode y máquina virtual.

- **El máximo se alcanza copiando la referencia.** "¿En qué año terminó
  el soporte oficial de Python 2?" (f1 = 0.960) reproduce la oración de
  la referencia palabra por palabra. El número mide parecido textual, no
  comprensión.

- **Los matices se pueden leer como contradicción.** "¿Cuándo se creó
  Python?" (f1 = 0.105) menciona 1989, cuando empezó el desarrollo, y
  luego fija 1991 como nacimiento oficial. Es más completa que la
  referencia ("Python fue creado en 1991."), pero al revisar a mano hay
  que resistir la tentación de anotar "contradicción" por el primer
  año que aparece.

- **La corrida no produjo ningún error factual**, así que el modo de
  falla clásico "un dato incorrecto puntúa alto" no se pudo verificar
  aquí: en la muestra no hubo ni un dato falso que puntuara alto.

## Muestra revisada

12 casos revisados a mano sobre 22 respuestas generadas el 21-11-2026
con `consultar_modelo` + `calcular_metricas` (modelo
`gemini-3.6-flash`). Selección: los **5 f1 más bajos** (0.023-0.105),
los **5 f1 más altos** (0.600-0.960) y **2 casos del medio** (0.182 y
0.258) elegidos a propósito por ser respuestas correctas de una sola
frase, para comprobar si la negación se penaliza. El registro completo,
con la rúbrica y una nota por caso, está en
`docs/revision_manual.json`.

Composición del dataset: 5 preguntas con respuesta libre, 13 con
instrucción de una sola frase, 4 sobre datos verificables (fechas,
versiones, nombres) y 4 de sí/no. Resultado de la revisión: **12/12
respuestas factualmente correctas, 11/12 completas y 0
contradicciones**. Como no hubo errores, el f1 no pudo distinguir
aciertos de errores: solo midió redacción.

## Recomendación de uso

- Usar `f1` solo para **comparar la misma consulta y la misma
  referencia** entre versiones de `consultar_modelo` (por ejemplo, con y
  sin la instrucción de brevedad). Nunca comparar f1 entre consultas
  distintas: la longitud de la referencia y la verbosidad de la
  respuesta dominan el número.
- Con la instrucción de una frase, un f1 >= 0.6 significa "dice lo
  mismo con otras palabras"; por debajo de 0.3 el número ya no distingue
  una respuesta correcta de una incorrecta (la de la tupla inmutable,
  correcta, saca 0.182).
- Revisar siempre a mano: (a) referencias con cifras, fechas o nombres
  propios; (b) el f1 **máximo** de la corrida, para confirmar que no es
  una copia literal sin comprensión; (c) cualquier f1 = 0, que puede ser
  respuesta vacía, error de la API o tema ausente del dataset.
- Evitar referencias con identificadores (`sys.path`,
  `scikit-learn`): `limpiar_texto` elimina los caracteres que no son
  `\w` ni espacio, así que esos tokens se fusionan y nunca coinciden con
  la respuesta del modelo.
