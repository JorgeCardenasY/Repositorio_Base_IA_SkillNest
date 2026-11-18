"""Suite de pruebas de ``src/cliente.py`` con mocks (pytest + unittest.mock).

Reglas que sigue toda la suite:

* **Nunca** se llama a la API real: el POST se reemplaza por un doble de prueba.
* Los ``patch`` apuntan a **cómo se ve** el objeto desde ``src/cliente.py``
  (``cliente.requests.post``, ``cliente.time.sleep``), no a la librería global;
  si se parchea ``requests.post`` a secas, el módulo sigue usando su propia
  referencia y el mock no tendría efecto.
* No se compara el valor exacto de la espera: el *jitter* es aleatorio y haría
  fallar la prueba al azar. Se verifica **cuántas veces** se llamó a ``time.sleep``.
* ``costo_total_sesion`` es estado global del módulo, así que una fixture
  ``autouse`` lo pone en cero antes y después de cada prueba.

Ejecución:
    pytest                      # pytest.ini apunta a esta suite
    pytest src/test_cliente.py -v
"""

from unittest.mock import Mock, patch

import pytest
import requests

import cliente
from cliente import consultar_modelo, con_reintento, enviar_peticion, registrar_costo


# --- utilidades ---------------------------------------------------------------


@pytest.fixture(autouse=True)
def costo_en_cero():
    """Deja ``costo_total_sesion`` en 0.0 antes y después de cada prueba.

    ``registrar_costo`` modifica un global del módulo; sin este reinicio, una
    prueba que suma costo contaminaría a la siguiente y el resultado dependería
    del orden de ejecución.
    """
    cliente.costo_total_sesion = 0.0
    yield
    cliente.costo_total_sesion = 0.0


def respuesta_falsa(status_code, datos=None):
    """Devuelve un doble de ``requests.Response`` con ese código y ese JSON.

    ``Mock`` ya hace que ``raise_for_status()`` no lance nada, que es lo que
    necesitamos para simular una respuesta correcta.
    """
    respuesta = Mock(status_code=status_code)
    respuesta.json.return_value = datos if datos is not None else {}
    return respuesta


# --- enviar_peticion ----------------------------------------------------------


@pytest.mark.parametrize("codigo", [401, 403])
def test_enviar_peticion_credencial_invalida(codigo):
    """401 y 403 deben salir como ``ValueError``.

    Es el caso "no tiene sentido reintentar": la credencial no sirve. Si esta
    clasificación se rompe, ``con_reintento`` gastaría cuota repitiendo una
    petición que siempre va a fallar, así que es la prueba más importante.
    """
    with patch("cliente.requests.post", return_value=respuesta_falsa(codigo)):
        with pytest.raises(ValueError, match="Credencial inválida"):
            enviar_peticion({"contents": [{"parts": [{"text": "prueba"}]}]})


def test_enviar_peticion_limite_de_uso():
    """429 debe salir como ``TimeoutError`` (transitorio: sí se reintenta).

    Se usa ``TimeoutError`` y no una excepción propia porque es el contrato que
    espera ``con_reintento`` para decidir que vale la pena volver a intentar.
    """
    with patch("cliente.requests.post", return_value=respuesta_falsa(429)):
        with pytest.raises(TimeoutError, match="no pudo procesar"):
            enviar_peticion({})


@pytest.mark.parametrize("codigo", [500, 502, 503])
def test_enviar_peticion_error_del_servidor(codigo):
    """Cualquier 500 o superior debe salir como ``TimeoutError``.

    Se parametriza con tres códigos para dejar claro que la condición es
    ``>= 500`` y no una lista cerrada de valores.
    """
    with patch("cliente.requests.post", return_value=respuesta_falsa(codigo)):
        with pytest.raises(TimeoutError, match="no pudo procesar"):
            enviar_peticion({})


def test_enviar_peticion_exito():
    """Una respuesta 200 devuelve el JSON **tal cual**, sin transformarlo.

    Se comprueba con ``is`` que el objeto devuelto es el mismo que entrega
    ``respuesta.json()``: el cliente no debe reconstruirlo ni filtrar claves.
    """
    datos = {
        "candidates": [{"content": {"parts": [{"text": "Santiago"}]}}],
        "usageMetadata": {"totalTokenCount": 15},
    }
    with patch(
        "cliente.requests.post", return_value=respuesta_falsa(200, datos)
    ) as mock_post:
        resultado = enviar_peticion({"contents": []})

    assert resultado is datos
    mock_post.assert_called_once()


def test_enviar_peticion_error_de_red_es_timeout():
    """Un ``ConnectionError`` de red también se clasifica como ``TimeoutError``.

    No es un código HTTP, pero el efecto para el usuario es el mismo: el
    proveedor no respondió y puede ser momentáneo.
    """
    with patch(
        "cliente.requests.post",
        side_effect=requests.exceptions.ConnectionError("sin red"),
    ):
        with pytest.raises(TimeoutError, match="No se pudo contactar"):
            enviar_peticion({})


def test_enviar_peticion_otro_4xx_no_esta_clasificado():
    """Un 400/404 no se clasifica: sube el ``HTTPError`` original de requests.

    Documenta el límite del cliente: sólo 401/403/429/5xx tienen tratamiento
    propio. ``con_reintento`` tampoco lo reintentará porque no es ``TimeoutError``.
    """
    respuesta = respuesta_falsa(400)
    respuesta.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "400 Client Error"
    )

    with patch("cliente.requests.post", return_value=respuesta):
        with pytest.raises(requests.exceptions.HTTPError):
            enviar_peticion({})


# --- con_reintento ------------------------------------------------------------


def test_con_reintento_espera_entre_intentos():
    """Un ``TimeoutError`` se reintenta y la segunda llamada devuelve el valor.

    El mock de ``time.sleep`` evita esperar de verdad (la prueba sería lenta) y
    se comprueba que se durmió exactamente una vez, sin mirar los segundos.
    """
    intentos = {"n": 0}

    def funcion_que_falla_una_vez():
        intentos["n"] += 1
        if intentos["n"] == 1:
            raise TimeoutError("simulado")
        return "ok"

    with patch("cliente.time.sleep") as mock_sleep:
        resultado = con_reintento(funcion_que_falla_una_vez)

    assert resultado == "ok"
    assert intentos["n"] == 2
    mock_sleep.assert_called_once()


def test_con_reintento_no_reintenta_value_error():
    """Sólo se reintenta ``TimeoutError``: un ``ValueError`` sube de inmediato.

    Es la garantía de que un 401/403 no gasta cuota: la función se llama una
    sola vez y ``time.sleep`` ni se toca.
    """
    funcion = Mock(side_effect=ValueError("credencial mala"))

    with patch("cliente.time.sleep") as mock_sleep:
        with pytest.raises(ValueError, match="credencial mala"):
            con_reintento(funcion)

    assert funcion.call_count == 1
    mock_sleep.assert_not_called()


def test_con_reintento_agota_intentos():
    """Al agotar los intentos se propaga la excepción **original**.

    Se verifica que sigue siendo ``TimeoutError``, que conserva su mensaje y que
    no se duerme después del último intento: con 3 intentos, 2 esperas.
    """
    funcion = Mock(side_effect=TimeoutError("siempre falla"))

    with patch("cliente.time.sleep") as mock_sleep:
        with pytest.raises(TimeoutError, match="siempre falla"):
            con_reintento(funcion, intentos=3)

    assert funcion.call_count == 3
    assert mock_sleep.call_count == 2


def test_con_reintento_exito_al_primer_intento_no_espera():
    """Si la función no falla, no se pierde tiempo esperando.

    Cubre el caso "todo bien", que ninguna prueba de error verifica.
    """
    with patch("cliente.time.sleep") as mock_sleep:
        assert con_reintento(lambda: "ok") == "ok"

    mock_sleep.assert_not_called()


def test_con_reintento_respeta_espera_maxima():
    """El backoff se corta en ``espera_maxima`` (+ hasta 10 % de jitter).

    Se compara con una **cota** (``<= 1.1``), nunca con un valor exacto: el
    jitter es aleatorio por diseño y una igualdad fallaría al azar.
    """
    funcion = Mock(side_effect=TimeoutError("x"))

    with patch("cliente.time.sleep") as mock_sleep:
        with pytest.raises(TimeoutError):
            con_reintento(funcion, intentos=3, espera_base=10, espera_maxima=1)

    esperas = [llamada.args[0] for llamada in mock_sleep.call_args_list]
    assert esperas and all(0 < espera <= 1.1 for espera in esperas)


# --- registrar_costo ----------------------------------------------------------


def test_registrar_costo_calcula():
    """1500 tokens con el precio referencial (0.002 por 1000) son 0.003.

    Se usa ``pytest.approx`` porque son ``float``: comparar con ``==`` haría
    la prueba frágil ante el redondeo binario.
    """
    costo = registrar_costo({"usageMetadata": {"totalTokenCount": 1500}})

    assert costo == pytest.approx(0.003)
    assert cliente.COSTO_POR_1000_TOKENS == pytest.approx(0.002)


def test_registrar_costo_acumula():
    """Dos operaciones de 1500 tokens dejan ``costo_total_sesion`` en 0.006.

    Es el estado que se muestra al final del script; si no acumulara, el
    reporte de la sesión siempre diría lo mismo que la última operación.
    """
    respuesta = {"usageMetadata": {"totalTokenCount": 1500}}

    registrar_costo(respuesta)
    registrar_costo(respuesta)

    assert cliente.costo_total_sesion == pytest.approx(0.006)


def test_registrar_costo_sin_metadata():
    """Si la respuesta no trae ``usageMetadata``, el costo es 0.0 y no revienta.

    Una respuesta recortada no debe tumbar la consulta completa: el texto sigue
    siendo útil aunque no se pueda estimar el gasto.
    """
    assert registrar_costo({}) == 0.0
    assert cliente.costo_total_sesion == 0.0


# --- consultar_modelo ---------------------------------------------------------


def test_consultar_modelo_convierte_error():
    """Un ``TimeoutError`` agotado se convierte en ``RuntimeError``.

    ``RuntimeError`` con mensaje en español es lo único que ve quien usa el
    módulo desde fuera; y se comprueba que se intentó 3 veces antes de rendirse.
    """
    with patch(
        "cliente.armar_peticion", return_value=("url", {"contents": []})
    ), patch(
        "cliente.enviar_peticion", side_effect=TimeoutError("429 simulado")
    ) as mock_enviar, patch("cliente.time.sleep"):
        with pytest.raises(RuntimeError, match="no respondió tras varios intentos"):
            consultar_modelo("¿Cuál es la capital de Chile?")

    assert mock_enviar.call_count == 3


def test_consultar_modelo_propaga_value_error():
    """Un ``ValueError`` (credencial inválida) sube **sin cambios**.

    No se convierte ni se reintenta: es un error de configuración y el mensaje
    original («Revisa tu GEMINI_API_KEY») es el que necesita ver el usuario.
    """
    with patch(
        "cliente.armar_peticion", return_value=("url", {"contents": []})
    ), patch(
        "cliente.enviar_peticion", side_effect=ValueError("Credencial inválida")
    ) as mock_enviar, patch("cliente.time.sleep") as mock_sleep:
        with pytest.raises(ValueError, match="Credencial inválida"):
            consultar_modelo("¿Cuál es la capital de Chile?")

    assert mock_enviar.call_count == 1
    mock_sleep.assert_not_called()


def test_consultar_modelo_exito_registra_costo_y_devuelve_texto():
    """Camino feliz: devuelve el texto, acumula el costo y no duerme.

    Une las tres piezas (envío, costo, extracción): si alguna se desconecta,
    esta prueba falla aunque las unitarias de cada función pasen.
    """
    datos = {"usageMetadata": {"totalTokenCount": 1500}}

    with patch(
        "cliente.armar_peticion", return_value=("url", {"contents": []})
    ), patch("cliente.enviar_peticion", return_value=datos), patch(
        "cliente.extraer_texto", return_value="Santiago"
    ), patch("cliente.time.sleep") as mock_sleep:
        assert consultar_modelo("¿Cuál es la capital de Chile?") == "Santiago"

    assert cliente.costo_total_sesion == pytest.approx(0.003)
    mock_sleep.assert_not_called()
