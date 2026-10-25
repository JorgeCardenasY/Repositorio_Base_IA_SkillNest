# README del repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

El presente es la documentación general para acceder al proyecto hasta su estado actual. Esrelevante mencionar que se espera que sea la misma estructura inicial, la cual se debiera ir nutriendo bloque a bloque, hasta llegar a la aplicación completa a entregar en el Gate 3.

## Cómo empezar

> Es relevante mencionar que he implementado parte del ejercicio utilizando la API de DeepSeek para comparativas.

Sigue las siguientes indicaciones:</br>
1. Instalar git y un IDE acorde a tu sistema operativo.
2. Obtén un API Key de Google Gemini (accede con tu cuenta a https://aistudio.google.com/api-keys).
3. Luego, clona este repositorio en tu máquina utilizando el comando bash/Terminal:</br>``` git clone https://github.com/JorgeCardenasY/Repositorio_Base_IA_SkillNest.git```

4. Crea tu entorno virtual de Python usando el comando ```python -m venv venv``` en tu terminal y actívalo utilizando 
WINDOWS ```venv/Scripts/activate```.
LINUX/iOS: ``` venv/bin/activate```.

5. Instala las dependencias del proyecto usando el comando ```pip install -r requirements.txt``` para poder usarlas en la aplicación.

6. Copia `.env.example` a un archivo nuevo llamado `.env` usando el comando ```Copy-Item .env.example .env``` (PowerShell) o ```cp .env.example .env``` (Linux/iOS), y completa ahí usando tu API y modelo. 

7. Para ejectuar la "aplicación", usa el comando ```python src/[SCRIPT].py```.
> Se han elaborado distintos scripts para el desarrollo del proyecto. Por favor, [continúa la lectura para conocerlos](#readme-de-los-ficheros-py).


## Estructura de carpetas y ficheros relevantes

- `src/` : almacena el código fuente del proyecto.
- `docs/` : documentación técnica del proyecto y de orientación en la fase de proyecto (**!= PRODUCCIÓN**).
- `tests/` : pruebas de código.
- `imgs/` : imagenes de prueba para la consulta de reconocimiento de patentes por IA.
- `requirements.txt` : listado dependencias de Python del proyecto. Facilita la reproductibilidad del entorno.
- `.env.example` : plantilla de las variables de entorno requeridas por el proyecto.
- `.gitignore` : restringe el acceso a los ficheros y carpetas listadas en el archivo `.gitignore`, de modo que no sean almacenados en el servidor Git.

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## BITACORA (A.K.A --> Registro del ensayo de instalación limpia)

- Fecha: 23/10/2026
- Encontrado: módulos faltantes.
- Corregido: Se incorporaron módulos faltantes en ficheros .py, los cuales se importan y se invocan.
- Resultado tras la corrección: aplicación funcional.

- Fecha: 22/10/2026
- Encontrado: En el README.md, no aparece el link del repositorio.
- Corregido: Se puso el link correcto del repositorio.
- Resultado tras la corrección: El repositorio se clonó de forma satisfactoria.

- Fecha: 23/10/2026
- Encontrado: No existían README para cada fichero.
- Corregido: Se agregan README para cada fichero, con enlace en README principal.
- Resultado tras la corrección: Robustecimiento de la documentación.


# README de los ficheros .py

Este índice lleva a la explicación de cada fichero Python del repositorio. La idea es la misma en todos: qué hace, cómo se usa y con qué hay que tener cuidado.

## Raíz

- [`app.py`](app.md): prueba inicial con `cowsay`.
- [`cliente.py`](cliente.md): helper de reintentos, en estado de borrador.

## src/

- [`armar_peticion.py`](docs/readmes/armar_peticion.md): arma la petición de texto.
- [`armar_peticion_imagen.py`](docs/readmes/armar_peticion_imagen.md): arma la petición con imagen.
- [`comparativa_pricing_hotel.py`](docs/readmes/comparativa_pricing_hotel.md): comparativa de texto entre modelos.
- [`comparativa_pricing_img.py`](docs/readmes/comparativa_pricing_img.md): comparativa con imagen de patente.
- [`consistencia.py`](docs/readmes/consistencia.md): 3 intentos por prompt y registro de resultados.
- [`consulta.py`](docs/readmes/consulta.md): flujo completo de una consulta.
- [`consulta_y_consumo.py`](docs/readmes/consulta_y_consumo.md): envío, extracción de texto y costo.
- [`consumir_gemini.py`](docs/readmes/consumir_gemini.md): latencia y costo de 4 consultas.
- [`parsear_respuesta.py`](docs/readmes/parsear_respuesta.md): texto del modelo -> diccionario.

## prompts/

- [`banco.py`](docs/readmes/banco.md): banco de prompts de prueba.

## Lectura sugerida

En orden a comprender de manera lógica el repositorio, tenga a bien aceptar la sugerencia de abordar el repositorio en este ŕoden: `consulta_y_consumo.md` -> `armar_peticion.md` -> `consulta.md`. Con esos tres se entiende el flujo base; el resto son variantes (imagen, comparativas, consistencia).
