# Decisión de arquitectura: elección de modelo
  
 ## Modelo elegido

 Inicialmente, el proyecto propuesto es la construcción de un chatbot para clientes de un hotel . Luego, y por acciones vinculadas a otra empresa, se está evaluando la posibilidad de implementar IA para procesos de procesamiento de imágenes y extracción de texto (OCR). Es por ello que se evalúan las capacidades de tres modelos de efecutar una consulta para :</br></br>
 __1.- Extracción de precio desde  una web (htps://hotelspalastaguas.cl ).</br>__
 __2.- Extracción de placa pantente desde imagen real extraída de internet.__

 Es relevante , respecto del segundo caso mencioando, que se efectuaron distintas pruebas con distintas imágenes (carpeta /img/), pero se eligión la imagen en la que la placa patente se visualiza incompleta y en ángulo, de modo de dificultar el proceso y hacerlo más cercano a un caso real.

Como antecedente, y en relación a lo arriba mencionado, mencionar que para facilitar la generación de la tabla final se elaboraron dos scripts (_comparativa_pricing_hotel.py_ y _comparativa_pricing_img.py_), los cuales se albergan en la carpeta src del repositorio.

  
 ## Diagrama de arquitectura

Para ambos casos, la infraestructura general de la consulta es la misma. A saber:

  ![Diagrama de Arquitectura](/docs/draw.io/app_diagram_BLOQUE_8_.drawio.png)

 ## Comparación de candidatos

> Modelo Identificando placa patente desde Imagen

| CRITERIO | MODELO 'GEMINI' | DeepSeek PRO | DeepSeek Flash |
|---|---|---|---|
| Placa extraída | BKV-834 | No se pudo extraer la placa porque la imagen no está disponible. | BKV-834 |
| Tokens entrada CONSUMIDOS | 1098 | 135 | 516 |
| Tokens Salida CONSUMIDOS | 6 | 387 | 253 |
| Costo por 1000 tokens de entrada | $0.0001 | $0.00132 | $0.0003 |
| Costo por 1000 tokens de Salida | $0.0003 | $0.00396 | $0.0012 |
| Total de la Consulta | $0.000149 | $0.001711 | $0.000458 |
| Latencia Observada | 20.53 s | 7.13 s | 2.70 s |
| Fecha de Medición | 2026-10-20 | 2026-10-20 | 2026-10-20 |

</br>

> Modelo señalando tarifas de Hotel según fuentes

| CRITERIO | MODELO 'GEMINI' | DeepSeek PRO | DeepSeek Flash |
|---|---|---|---|
| Respuesta | Error | USD 50 / CLP $45.000 | USD 35 / CLP 33.000 |
| Tokens entrada CONSUMIDOS | Error | 155 | 102 |
| Tokens Salida CONSUMIDOS | Error | 2917 | 3269 |
| Costo por 1000 tokens de entrada | $0.0001 | $0.00132 | $0.0003 |
| Costo por 1000 tokens de Salida | $0.0003 | $0.00396 | $0.0012 |
| Total de la Consulta | Error | $0.011756 | $0.003953 |
| Latencia Observada | Error | 38.58 s | 17.07 s |
| Fecha de Medición | 2026-10-20 | 2026-10-20 | 2026-10-20 |
                                                               

 ## Justificación

La calidad de las respuestas obtenidas son diversas , ya que en el primer caso de uso , puede verse que hay dos respuestas correctas y una de error. También, es importante mencionar que si bien gemini-flash tiene un precio potencialmente menor, la latencia de respuesta es de aproximadamente 8 veces la de DeepSeek Flash. Respecto de ésta, es importante mencionar que su precio es aproximadament el triple de la de Gemini. Respecto del modelo DeepSeek Pro, el manejo de errores imprime en pantalla una indicación que no apunta a al situación real. A saber, este modelo (DeepSeek PRO), según la documentación, no soportaría el manejo de imágenes.

Respecto del Segundo Caso de Uso reportado (Consulta sobre datos de Hotel), en relación a la calidad de las respuestas, los modelos de DeepSeek presentan respuestas distintas ante el mismo problema, y de Gemini, se responde con respuesta tipo Error (Demasiadas Consultas).
En relación a las latencias de respuesta el modelo pro de DeepSeek se tomó más del doble de tiempo en comparación con el modelo flash. Caso similar acontece con los precios, en los que la versión pro pondera casi cuatro veces más que la flash.


Con todo, y ante los datos presentes, en lrelación a los modelos comparados en el ejercicio, debemos concluir que:


 ## Alternativa descartada y por qué

 En relación al primer caso de uso, en las pruebas ejecutadas respecto del reconocimiento de patentes, los modelos gemini-flash y DeepSeek Flash lograron ejecutar con calidad la consulta, no obstante Gemini se tomó un tiempo considerablemente mayor en relación a DeepSeek Flash, modelo que logró el reconocimiento en misma calidad pero con un _pricing_ mayor y en menor tiempo. Por ello, y ante los datos de la prueba, se consideraría el uso de DeepSeek Flash para el reconocimiento de imágenes para una respuesta que privilegie el tiempo.

En relación al segundo caso de uso, extracción de datos de un hotel en específico,  puede verse que el modelo DeepSeek Flash brindó una respuesta rápida pero alucinada, por lo que se consideraría DeepSeek Pro para obtención de datos desde una web específica. A este caso de uso y en base a los datos obtenidos no podemos concluir ni favorable ni neativamente en relación a Gemini debido al exceso de consultas fectuadas desde mi IP.

Atte.-

Jorge Cárdenas Yañez </br>
20-10-2026