# README del repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

El presente es la documentación general para acceder al proyecto hasta su estado actual. Esrelevante mencionar que se espera que sea la misma estructura inicial, la cual se debiera ir nutriendo bloque a bloque, hasta llegar a la aplicación completa a entregar en el Gate 3.

## Cómo empezar

Si gue las siguientes indicaciones:

1. Clona este repositorio utilizando el comando "git clone https://github.com/SebaPobando/gate-1.git"
2. Crea tu entorno virtual de Python usando el comando <python -m venv venv> en tu terminal y actívalo usando el comando <venv/Scripts/activate>.
3. Instala las dependencias del proyecto usando el comando <pip install -r requirements.txt> para poder usarlas en la aplicación.
4. Copia `.env.example` a un archivo nuevo llamado `.env` usando el comando <Copy-Item .env.example .env>, y completa ahí usando tu API.
5. Para ejectuar la "aplicación", usa el comando <python src/consumir_gemini.py>.

## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Registro del ensayo de instalación limpia
 
- Fecha: 22/10/2026
- Encontrado: En el README.md, no aparece el link del repositorio.
- Corregido: Se puso el link correcto del repositorio.
- Resultado tras la corrección: El repositorio se clonó de forma satisfactoria.

# README de los ficheros .py

Este índice lleva a la explicación de cada fichero Python del repositorio. La idea es la misma en todos: qué hace, cómo se usa y con qué hay que tener cuidado.

## Raíz

- [`app.py`](app.md): prueba inicial con `cowsay`.
- [`cliente.py`](cliente.md): helper de reintentos, en estado de borrador.

## src/

- [`armar_peticion.py`](armar_peticion.md): arma la petición de texto.
- [`armar_peticion_imagen.py`](armar_peticion_imagen.md): arma la petición con imagen.
- [`comparativa_pricing_hotel.py`](comparativa_pricing_hotel.md): comparativa de texto entre modelos.
- [`comparativa_pricing_img.py`](comparativa_pricing_img.md): comparativa con imagen de patente.
- [`consistencia.py`](consistencia.md): 3 intentos por prompt y registro de resultados.
- [`consulta.py`](consulta.md): flujo completo de una consulta.
- [`consulta_y_consumo.py`](consulta_y_consumo.md): envío, extracción de texto y costo.
- [`consumir_gemini.py`](consumir_gemini.md): latencia y costo de 4 consultas.
- [`parsear_respuesta.py`](parsear_respuesta.md): texto del modelo -> diccionario.

## prompts/

- [`banco.py`](banco.md): banco de prompts de prueba.

## Lectura sugerida

En orden a comprender de manera lógica el repositorio, tenga a bien aceptar la sugerencia de abordar el repositorio en este ŕoden: `consulta_y_consumo.md` -> `armar_peticion.md` -> `consulta.md`. Con esos tres se entiende el flujo base; el resto son variantes (imagen, comparativas, consistencia).
