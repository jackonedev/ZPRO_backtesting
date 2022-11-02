"""https://polygon.io/docs/forex/getting-started

    Limitaciones de la API: solo tengo data de los últimos 2 años

"""

import requests
import pandas as pd
import datetime as dt


def fx_symbol_candles(
    forexTicker: str, multiplier: str, timespan: str, fromS: str, toS: str, apikey: str
) -> pd.DataFrame:
    """
    Possible Entrys:
        - forexTicker: e.g. format: 'EURUSD'
        - multiplier: any int bigger than 1 in string format
        - timespan: 'minute', 'hour', 'day', 'week', 'month'
        - fromS, toS: format '%Y-%m-%d' - consider use module function for this parameters
        - apikey: apikey

    return:
        pandas.DataFrame with results
    """
    function = "/aggs"
    default_params = "adjusted=true&sort=asc&limit=50000"

    URL_BASE = f"https://api.polygon.io/v2{function}"

    URL_BASE += f"/ticker/C:{forexTicker}/range/{multiplier}/{timespan}/{fromS}/{toS}"
    URL_BASE += f"?{default_params}&apiKey={apikey}"

    r = requests.get(URL_BASE)
    js = r.json()

    df = pd.DataFrame(js["results"])
    try:
        df["date"] = pd.to_datetime(df["t"], unit="ms")
    except:
        df["date"] = pd.to_datetime(df["t"])
    df.set_index("date", inplace=True)
    df.drop(columns="t", inplace=True)
    df.rename(
        columns=dict(
            zip(
                df.columns,
                ["Volume", "VolWeiAvgPrc", "Open", "Close", "High", "Low", "Qtx"],
            )
        ),
        inplace=True,
    )
    df = df.reindex(
        ["Close", "High", "Low", "Open", "Volume", "Qtx", "VolWeiAvgPrc"], axis=1
    )
    if sum(df["Volume"] - df["Qtx"]) == 0:
        df.drop(columns="Qtx", inplace=True)
    return df


def convert_to_timestamp(dateDT: str) -> dt.datetime.timestamp:
    return int(dt.datetime.timestamp(dateDT)) * 1000


def restar_horas(fecha):
    """Esto funciona para temporalidad inferior (Horario - Minutos) - to testeado"""
    if isinstance(fecha, str):
        fecha = dt.datetime.strptime(fecha, "%Y-%m-%d")
    fecha -= dt.timedelta(hours=720)  # window
    fecha = dt.datetime.strftime(fecha, "%Y-%m-%d")
    return fecha


def restar_dias(fecha):
    """Esto funciona para temporalidad mayor (Mensual - Semanal - Diario) - to testeado"""
    if isinstance(fecha, str):
        fecha = dt.datetime.strptime(fecha, "%Y-%m-%d")
    fecha -= dt.timedelta(days=90)
    fecha = dt.datetime.strftime(fecha, "%Y-%m-%d")
    return fecha


def reset_fechas(df, func):
    """Esta funcion es para la window horaria y la window diaria, devuelve el lapso de tiempo anterior al recientemente llamado (call)"""
    fecha_inicio = df.index[0]
    fecha_final = fecha_inicio - dt.timedelta(days=1)
    fecha_final = dt.datetime.strftime(fecha_final, "%Y-%m-%d")
    return func(fecha_inicio), fecha_final


## CEMENTERIO

# 2) Cuando automatizo las calls me desconoce la API

# def fx_symbol_candles(forexTicker, multiplier, timespan, fromS, toS, apikey):
#     """
#     timespan's: minute, hour, day, week, month
#     fromS, toS: need format %Y-%m-%d

#       obsoleto:
#          {'status': 'ERROR', 'request_id': '2012ee028cbed672b1fc3dc6fd33617b', 'error': 'Unknown API Key'}
#           "Error en el call: 'results'"
#     """
#     function = '/aggs'
#     default_params = "adjusted=true&sort=asc&limit=50000"

#     URL_BASE = f'https://api.polygon.io/v2{function}'


#     fromDT = dt.datetime.strptime(fromS, '%Y-%m-%d')
#     toDT = dt.datetime.strptime(toS, '%Y-%m-%d')


def seccionador_fechas(fecha_i, fecha_f, timespan):
    fechas = []
    while fecha_i < fecha_f:
        fromTS = convert_to_timestamp(fecha_i)
        if timespan == "month" or timespan == "week" or timespan == "day":
            fecha_i += dt.timedelta(days=700)
            toTS = fecha_i
        elif timespan == "hour" or timespan == "minute":
            fecha_i += dt.timedelta(hours=1400)
            toTS = fecha_i

        if toTS > fecha_f:
            fechas.append((fromTS, convert_to_timestamp(fecha_f)))
        else:
            fechas.append((fromTS, convert_to_timestamp(toTS)))
    return fechas


#     lapsos = seccionador_fechas(fromDT, toDT, timespan)

#     df = pd.DataFrame()
#     for fecha_i, fecha_f in lapsos:
#         URL_BASE += f'/ticker/C:{forexTicker}/range/{multiplier}/{timespan}/{fecha_i}/{fecha_f}'
#         URL_BASE += f'?{default_params}&apiKey={apikey}'
#         r = requests.get(URL_BASE)
#         js = r.json()
#         try:
#             df.append(pd.DataFrame(js["results"]))
#         except Exception as e:
#             print (js)
#             return f"Error en el call: {e}"
#         sleep(20)

#     try:
#         df['date'] = pd.to_datetime(df['t'], unit='ms')
#     except:
#         df['date'] = pd.to_datetime(df['t'])
#     df.set_index('date', inplace=True)
#     df.drop(columns="t", inplace=True)
#     df.rename(columns=dict(zip(df.columns, ["Volume", "VolWeiAvgPrc", "Open", "Close", "High", "Low", "Ntx"])), inplace=True)
#     df = df.reindex(["Close", "High", "Low","Open", "Volume", "Ntx", "VolWeiAvgPrc"], axis=1)
#     if sum(df["Volume"] - df["Ntx"]) == 0:
#         df.drop(columns="Ntx", inplace=True)
#     return df
