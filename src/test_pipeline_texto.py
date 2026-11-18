

from pipeline_texto import procesar_texto


def test_procesar_texto_normaliza_mayusculas_y_puntuacion():
    resultado = procesar_texto("El Cielo, es AZUL!")

    assert resultado == ["el", "cielo", "es", "azul"]

def test_procesar_texto_solo_puntuacion_devuelve_lista_vacia():
    resultado = procesar_texto("¡¡¡...!!!")

    assert resultado == []


print(f"test_procesar_texto_normaliza_mayusculas_y_puntuacion(): {test_procesar_texto_normaliza_mayusculas_y_puntuacion()}")
print(f"test_procesar_texto_solo_puntuacion_devuelve_lista_vacia(): {test_procesar_texto_solo_puntuacion_devuelve_lista_vacia()}")