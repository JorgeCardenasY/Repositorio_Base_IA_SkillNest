import time
from typing import Callable, Any
from src.consulta_y_consumo import extraer_texto

def con_reintento(  #función, intentos, espera_segundos. Return--> CUALQUIERA
    funcion: Callable[[], Any],
    intentos: int = 3,
    espera_segundos: int = 2
    ) -> Any:
    for intento in range(intentos):
        try:
            return funcion()
        except TimeoutError as e:
            if intento == intentos - 1:
                raise
            print(f"Intento {intento + 1} de {intentos} falló por límite de uso/servidor. Reintentando en {espera_segundos} segundos...")
            time.sleep(espera_segundos)






    #ITERAR LA cantidad de intentos
    # INTENTAR EJECUTAR LA FUNCION
        # TimeoutError:
        # raise


        #Espera
        #time.sleep(cantidad_segundos)