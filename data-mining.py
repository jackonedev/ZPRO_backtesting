
from time import sleep
from apps.forex_api.polygon import fx_symbol_candles, restar_horas, restar_dias, reset_fechas
import pandas as pd
import os
from dotenv import load_dotenv
import datetime as dt
import apps.tools as tlz
from itertools import count

def mining(activo, multiplicador, timespan, TOKEN):

    fecha_actual = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d')
    if timespan == 'hour' or timespan == "minute":
        temporalidad = 'inferior'
    elif timespan == 'day' or timespan == "week" or timespan == "month":
        temporalidad == 'mayor'


    iteracion = count(1)
    
    df = fx_symbol_candles(
        activo, multiplicador, timespan, restar_horas(fecha_actual), fecha_actual, TOKEN
    )
    next(iteracion)

    while True:
        print (f"iteracion nº {next(iteracion)}")
        try:
            # GUARDADO
            if multiplicador != "1":
                tlz.descargar_csv(
                    frame=df, 
                    dir_name=f"fx_historico\\temp_{temporalidad}", 
                    prefix=activo, 
                    suffix=f"{multiplicador}{timespan}",
                    fix=True
                    )
            else:
                tlz.descargar_csv(
                    frame=df, 
                    dir_name=f"fx_historico\\temp_{temporalidad}", 
                    prefix=activo, 
                    suffix=f"{timespan}",
                    fix=True
                    )

            # PROCESADO
            fecha_i, fecha_f = reset_fechas(df, restar_horas)
            df = pd.concat(
                [
                    fx_symbol_candles(
                        activo, 
                        multiplicador, 
                        timespan, 
                        fecha_i, 
                        fecha_f, 
                        TOKEN
                        ),
                    df,
                ]
            )

            # free API
            sleep(21)

        except:
            print ('Data Mining process ended')
            break


def main():
    load_dotenv()
    
    done_t_inf = ['EURNZD', "EURCAD"]

    TOKEN3 = os.environ["TOKEN_PG"]
    activo = "EURUSD"
    multiplicador = str(1)
    timespan = "minute"

    mining(activo=activo, multiplicador=multiplicador, timespan=timespan, TOKEN=TOKEN3)


if __name__ == "__main__":
    main()
