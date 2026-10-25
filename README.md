# README del repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

## Qué hace

El presente es la documentación general para acceder al proyecto hasta su estado actual. Es relevante mencionar que se espera que sea la misma estructura inicial, la cual se debiera ir nutriendo bloque a bloque, hasta llegar a la aplicación completa a entregar en el Gate 3.

> Es relevante mencionar que, además de las indicaciones específicas de Google Gemini que se han dado durante la capacitación, he implementado parte del ejercicio utilizando la API de DeepSeek para comparativas para simular casos reales de uso de mi quehacer laboral.

## Estado

## Requisitos

Sigue las siguientes indicaciones:</br>
1. Instalar git y un IDE acorde a tu sistema operativo.

2. Obtén una llave de Google Gemini en https://aistudio.google.com/api-keys. Para las comparativas también necesitas una de DeepSeek: https://platform.deepseek.com/api_keys.

## Cómo empezar (instalación)

3. Luego, clona este repositorio en tu máquina utilizando el comando bash/Terminal:

   ```bash
   git clone https://github.com/JorgeCardenasY/Repositorio_Base_IA_SkillNest.git
   ```

4. Crea tu entorno virtual de Python y actívalo:

   ```bash
   python -m venv venv
   ```

   - Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
   - Windows (CMD): `venv\Scripts\activate.bat`
   - Linux/macOS: `source venv/bin/activate`

5. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

## Variables de entorno

6. Copia `.env.example` a un fichero nuevo llamado `.env`:

   ```bash
   cp .env.example .env
   ```

   En PowerShell: `Copy-Item .env.example .env`. Luego completa las llaves y modelos (Gemini y, si vas a usar las comparativas, DeepSeek).

## Scripts y costo en consultas

7. Ejecuta el script que quieras probar:

   | Comando | Qué hace | Consultas reales |
   |---|---|---|
   | `python src/consulta.py` | Una consulta con respuesta JSON | 1 |
   | `python src/consulta_y_consumo.py` | Ejemplo mínimo de envío y costo | 1 |
   | `python src/consumir_gemini.py` | Latencia promedio y costo | 4 |
   | `python src/consistencia.py` | 3 intentos por prompt (2 prompts) | 6 |
   | `python src/comparativa_pricing_hotel.py` | Gemini vs DeepSeek, texto | 3 |
   | `python src/comparativa_pricing_img.py imgs/patente1.jpg` | Gemini vs DeepSeek, imagen | 3 |
   | `python app.py` | Prueba con `cowsay` | 0 |

   `cliente.py` es un helper: no se ejecuta solo.

## Estructura de carpetas

- `src/` : almacena el código fuente del proyecto.
- `docs/` : documentación técnica del proyecto y de orientación en la fase de proyecto (**!= PRODUCCIÓN**).
- `tests/` : aún sin pruebas automatizadas.
- `imgs/` : imagenes de prueba para la consulta de reconocimiento de patentes por IA.
- `requirements.txt` : listado dependencias de Python del proyecto. Facilita la reproductibilidad del entorno.
- `.env.example` : plantilla de las variables de entorno requeridas por el proyecto.
- `.gitignore` : restringe el acceso a los ficheros y carpetas listadas en el archivo `.gitignore`, de modo que no sean almacenados ni publicados en el servidor Git.

## Documentación

Cada fichero `.py` tiene su propio README con qué hace, cómo se usa y con qué hay que tener cuidado. El índice completo, con la lectura sugerida, está en [`docs/readmes/README.md`](docs/readmes/README.md).

## Salidas

## Problemas conocidos

> Cada consulta consume cuota. Si aparece un 429, espera o cambia `MODELO` en el `.env`. `consistencia.py` no tiene guardia `__main__`: se ejecuta al importarlo.

## Reglas y seguridad

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Bitácora — Registro del ensayo de instalación limpia

> **Fecha: 22/10/2026**
- Encontrado: librerías no actualizadas en requirements.txt.
- Corregido: `pip freeze > requirements.txt`.
- Resultado tras la corrección: Reproductibilidad de repositorio.

> **Fecha: 22/10/2026**
- Encontrado: En el README.md, no aparece el link del repositorio.
- Corregido: Se puso el link correcto del repositorio.
- Resultado tras la corrección: El repositorio se clonó de forma satisfactoria.

> **Fecha: 23/10/2026**
- Encontrado: módulos faltantes.
- Corregido: Se incorporaron módulos faltantes en ficheros .py (v.g.: armar_peticion.py, parsear_respuesta.py, entre otros), los cuales se importan y se invocan.
- Resultado tras la corrección: aplicación funcional.

> **Fecha: 23/10/2026**
- Encontrado: No existían README para cada fichero.
- Corregido: Se agregan README para cada fichero, con enlace en README principal.
- Resultado tras la corrección: Robustecimiento de la documentación.

> **Fecha: 24/10/2026**
- Encontrado: Fichero README de la raíz del proyecto con información que distrae de una vista general del proyecto.
- Corregido: Se eliminó el índice duplicado del README principal y se enlazó `docs/readmes/README.md`.
- Resultado tras la corrección: README principal más breve y con enlaces válidos a la documentación por fichero.

> **Fecha: 24/10/2026**
- Encontrado: Fichero `.env.example` no actualizado.
- Corregido: Se actualiza `.env.example`.
- Resultado tras la corrección: Reproductibilidad del repositorio.


> **Fecha: 24/10/2026**
- Encontrado: `.gitignore` estaba pasando ficheros en subdirectorio `.postman`.
- Corregido: Se actualiza la regla en `.gitignore`.
- Resultado tras la corrección: Reproductibilidad del repositorio.

> **Fecha: 24/10/2026**
- Encontrado: El README principal no seguía el orden acordado y la sección de pruebas no reflejaba su estado real.
- Corregido: Se reordenaron las secciones y se indicó que `tests/` aún no tiene pruebas automatizadas.
- Resultado tras la corrección: README con la estructura acordada y la sección de pruebas actualizada.

> **Fecha: 24/10/2026**
- Encontrado: `.postman/resources.yaml` seguía versionado pese a la regla de `.gitignore`.
- Corregido: Se dejó de trackear con `git rm --cached .postman/resources.yaml`.
- Resultado tras la corrección: El archivo queda ignorado y fuera del repositorio, sin borrarlo del disco.

> **Fecha: 24/10/2026**
- Encontrado: `prompts/registro.json` conservaba una corrida fallida e incompleta.
- Corregido: Se regeneró el registro de ambos prompts con `gemini-flash-latest` y reintentos espaciados.
- Resultado tras la corrección: Registro completo: `HotelAmaru` 3/3 y `HotelSpaLasTaguas` 1/3 (dos intentos con 429).

## Autor
