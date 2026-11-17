# README del repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

## Qué hace

El presente es la documentación general para acceder al proyecto hasta su estado actual. Es relevante mencionar que se espera que sea la misma estructura inicial, la cual se debiera ir nutriendo bloque a bloque, hasta llegar a la aplicación completa a entregar en el Gate 3.

> Es relevante mencionar que, además de las indicaciones específicas de Google Gemini que se han dado durante la capacitación, he implementado parte del ejercicio utilizando la API de DeepSeek para comparativas para simular casos reales de uso de mi quehacer laboral.

## Estado


Repositorio base **operativo en local** y en fase de ejercicios previa al Gate 3. Última verificación registrada en la bitácora: **17/11/2026**.

| Área | Estado | Evidencia |
|---|---|---|
| Consulta a Gemini | ✅ Operativa | `src/consulta.py` |
| Costo y latencia | ✅ Operativos | `src/consulta_y_consumo.py`, `src/consumir_gemini.py` |
| Consistencia | 🟡 Implementada; última corrida: `HotelAmaru` 3/3 y `HotelSpaLasTaguas` 1/3 | `prompts/registro.json` |
| Comparativas Gemini/DeepSeek | ✅ Operativas | `src/comparativa_pricing_hotel.py`, `src/comparativa_pricing_img.py` |
| Documentación por fichero | ✅ 17 fichas | `docs/readmes/` |
| Pruebas automatizadas | ✅ 20 casos en pytest | `test_cliente.py`, `src/test_cliente.py` |


Pendiente además: integración continua y empaquetado. Las limitaciones y fallos conocidos se detallan en [Problemas conocidos](#problemas-conocidos).



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
   | `python src/cliente_reintento.py` | Una consulta con reintentos y backoff | 1 (hasta 3 si hay 429) |
   | `python src/cliente_reintento_rate_limit.py` | 10 consultas iguales seguidas para provocar el 429 | 10 (hasta 30 si hay 429) |
   | `python src/consulta_y_consumo.py` | Ejemplo mínimo de envío y costo | 1 |
   | `python src/consumir_gemini.py` | Latencia promedio y costo | 4 |
   | `python src/consistencia.py` | 3 intentos por prompt (2 prompts) | 6 |
   | `python src/comparativa_pricing_hotel.py` | Gemini vs DeepSeek, texto | 3 |
   | `python src/comparativa_pricing_img.py imgs/patente1.jpg` | Gemini vs DeepSeek, imagen | 3 |
   | `python cliente.py` | Cliente modular: una consulta con reintentos, costo y texto | 1 (hasta 3 si hay 429) |
   | `python src/cliente.py` | El mismo cliente en versión de `src/` | 1 (hasta 3 si hay 429) |
   | `python app.py` | Prueba con `cowsay` | 0 |

   Las suites de pruebas (`test_cliente.py`) no hacen consultas reales: ver [Pruebas automatizadas](#pruebas-automatizadas).

## Estructura de carpetas

- `src/` : almacena el código fuente del proyecto.
- `docs/` : documentación técnica del proyecto y de orientación en la fase de proyecto (**!= PRODUCCIÓN**).
- `tests/` : reservado para pruebas de integración; las unitarias viven junto al código (`test_cliente.py`).
- `imgs/` : imagenes de prueba para la consulta de reconocimiento de patentes por IA.
- `requirements.txt` : listado dependencias de Python del proyecto. Facilita la reproductibilidad del entorno.
- `pytest.ini` : configuración mínima de pytest; apunta la corrida por defecto a `test_cliente.py`.
- `.env.example` : plantilla de las variables de entorno requeridas por el proyecto.
- `.gitignore` : restringe el acceso a los ficheros y carpetas listadas en el archivo `.gitignore`, de modo que no sean almacenados ni publicados en el servidor Git.

## Documentación

Cada fichero `.py` tiene su propio README con qué hace, cómo se usa y con qué hay que tener cuidado. El índice completo, con la lectura sugerida, está en [`docs/readmes/README.md`](docs/readmes/README.md).

## Pruebas automatizadas

La suite del cliente usa **pytest** y no consume cuota: reemplaza `requests.post`, `time.sleep` y las funciones del proyecto por dobles de prueba, así que no hace ninguna llamada real.

```bash
pip install -r requirements.txt   # ya incluye pytest
pytest                            # suite canónica (raíz): 20 casos
pytest src/test_cliente.py -v     # la misma suite sobre src/cliente.py
```

Qué cubre cada caso, y por qué se mockea así, está en [`docs/readmes/test_cliente.md`](docs/readmes/test_cliente.md).

## Salidas

La mayoría de los comandos **imprimen en consola** y no generan ficheros. El único artefacto de datos que escribe el código es `prompts/registro.json`, que `consistencia.py` reescribe en cada corrida. Python puede crear `__pycache__/`, que está ignorado por Git.

| Comando | Salida en consola | Fichero generado |
|---|---|---|
| `python src/consulta.py` | Texto crudo del modelo + campos `categoria`, `confianza`, `explicacion` | Ninguno |
| `python src/cliente_reintento.py` | Texto crudo + campos + nº de intento + costo estimado | Ninguno |
| `python src/cliente_reintento_rate_limit.py` | Costo por consulta, `Respuesta i: …` y costo total del ensayo | Ninguno |
| `python src/consulta_y_consumo.py` | Costo estimado en USD + respuesta | Ninguno |
| `python src/consumir_gemini.py` | 4 latencias, promedio y costo de la última consulta | Ninguno |
| `python src/consistencia.py` | Respuestas/errores por intento + resumen `exitos/intentos` | `prompts/registro.json` |
| `python src/comparativa_pricing_hotel.py` | Métricas por modelo + tabla Markdown comparativa | Ninguno |
| `python src/comparativa_pricing_img.py imgs/patente1.jpg` | Placa extraída + métricas + tabla Markdown | Ninguno |
| `python cliente.py` | Costo de la operación y acumulado + respuesta | Ninguno |
| `python src/cliente.py` | Igual que `cliente.py` (espejo en `src/`) | Ninguno |
| `python app.py` | Dos bloques ASCII de `cowsay` | Ninguno |

`prompts/registro.json` tiene esta forma:

```json
{
  "HotelAmaru": {
    "exitos": 3,
    "intentos": 3
  },
  "HotelSpaLasTaguas": {
    "exitos": 1,
    "intentos": 3
  }
}
```

## Problemas conocidos

> Cada consulta consume cuota. Si aparece un 429, espera o cambia `MODELO` en el `.env`. `consistencia.py` no tiene guardia `__main__`: se ejecuta al importarlo.

> `cliente.py` (raíz) y `src/cliente.py` son copias espejo del mismo cliente: si corriges uno, replica el cambio en el otro. Sus dos suites se llaman igual, así que se ejecutan por separado (`pytest` corre la de la raíz; `pytest src/test_cliente.py`, la de `src/`). La versión de referencia de la política de reintentos sigue siendo `src/cliente_reintento.py`.

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

> **Fecha: 15/11/2026**
- Encontrado: `src/cliente_reintento.py` mezclaba un mock con el cliente real, arrancaba código a nivel de módulo y fallaba con `NameError` al ejecutarse.
- Corregido: se reescribió como capa de reintentos sobre `consulta_y_consumo.enviar_peticion`, con clasificación de errores, backoff exponencial con jitter, validación de `.env`, `main()` y guardia `__main__`; se agregó su ficha en `docs/readmes/cliente_reintento.md`.
- Resultado tras la corrección: compilación, import sin efectos y política de reintentos verificadas con un doble de prueba. La consulta real quedó pendiente: el proveedor rechazó la `GEMINI_API_KEY` del `.env` (HTTP 401, "API key not valid") y el script lo reportó como error definitivo, sin reintentar.

> **Fecha: 16/11/2026**
- Encontrado: `src/cliente_reintento_rate_limit.py` tenía el bloque original entrecomillado (código muerto, líneas 1-63) y el bloque activo con indentación mixta (1 espacio, espacios+tab y tabulaciones), por lo que no compilaba (`IndentationError` en `import os`, `TabError` en la línea 95). Además importaba `armar_peticion` y `extraer_texto` desde `cliente_api`, que no las define, y desarmaba mal la tupla de `armar_peticion`. Su `enviar_peticion` local usaba `timeout=10` y un modelo hardcodeado, ignorando `MODELO` del `.env`.
- Corregido: se eliminó el bloque muerto, se reindentó el bloque activo a 4 espacios y se reescribió sobre el cliente del proyecto (`armar_peticion` + `consulta_y_consumo.enviar_peticion`, con `timeout=60` y `Retry-After`), convirtiendo `HTTPError` (400/404) en `RuntimeError` y reportando `ValueError` (401/403) sin traceback; se agregó su ficha en `docs/readmes/cliente_reintento_rate_limit.md` y su entrada en el índice.
- Resultado tras la corrección: `tabnanny`, `compile`, import y el bucle completo de 10 consultas verificados con un doble de prueba (HTTP 200, 429, 503, 400, 404, 403 y caída de red), sin gastar cuota. La corrida real quedó pendiente de cuota.

> **Fecha: 17/11/2026**
- Encontrado: `cliente.py` (raíz) seguía siendo un borrador (imports duplicados de `cliente_api`, `consumir_gemini` y `consulta_y_consumo`, `armar_peticion` llamada con 3 argumentos y sin `enviar_peticion`); `src/test_cliente.py` usaba `con_reintento` sin importarlo y no existía un módulo `cliente` importable desde `src/`; pytest no estaba instalado ni declarado en `requirements.txt`.
- Corregido: se reescribieron `cliente.py` y su espejo `src/cliente.py` con las cuatro funciones (`enviar_peticion`, `con_reintento`, `registrar_costo`, `consultar_modelo`) y la clasificación 401/403 → `ValueError`, 429/5xx → `TimeoutError`; se ampliaron las dos suites a 17 pruebas (20 casos) con docstrings explicativos; se agregó `pytest` al `requirements.txt`, `.pytest_cache/` al `.gitignore`, un `pytest.ini` y las fichas `cliente.md`, `cliente_src.md` y `test_cliente.md`.
- Resultado tras la corrección: `pytest`, `pytest test_cliente.py -v` y `pytest src/test_cliente.py -v` dan 20 casos aprobados cada uno, sin tráfico de red; se comprobó con un plugin temporal que cada suite importa su propio módulo (`cliente.py` y `src/cliente.py`).

## Autor

Atte.-

Jorge Cárdenas Yañez </br>
[HitGub](https://github.com/JorgeCardenasY)</br>
[LinkedIn](https://www.linkedin.com/in/jorgecardenasy/) </br>
[eLabs.cl](https://www.elabs.cl/) </br>