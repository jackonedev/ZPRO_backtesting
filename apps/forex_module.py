""""
ESTE ARCHIVO ESTA TOTALMENTE OBSOLETO, HA SIDO DIVIDO EN UN SUBPAQUETE

LA RAZON DE CONSERVARLO ES POR LAS PRUEBAS QUE SE EJECUTAN EN EL __name__ == '__main__'

CON MOTIVO DE USARSE COMO MATERIAL PARA LA DOCUMENTACION

"""


"""https://www.alphavantage.co/documentation/"""
# TODO: finnhub documentation

import os
from dotenv import load_dotenv  # remember: pip install python-dotenv
import requests
import pandas as pd
from datetime import datetime
import datetime as dt


def fx_price(function, from_symbol, to_symbol, api_key, outputsize="full"):
    """API SERVICE OF ALPHA VANTAGE

    Keyword arguments:
    function = FX_DAILY, FX_WEEKLY, FX_MONTHLY
    from_symbol: first asset
    to_symbol: second asset
    api_key: personal TOKEN
    outputsize: "full", "compact",
    Return: pandas.DataFrame
    """

    URL_BASE = "https://www.alphavantage.co/query"

    parametros = {
        "function": function,
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": outputsize,
        "apikey": api_key,
    }

    r = requests.get(URL_BASE, params=parametros)
    data = r.json()

    if function == "FX_DAILY":
        data = pd.DataFrame(data["Time Series FX (Daily)"]).T
    elif function == "FX_WEEKLY":
        data = pd.DataFrame(data["Time Series FX (Weekly)"]).T
    elif function == "FX_MONTHLY":
        data = pd.DataFrame(data["Time Series FX (Monthly)"]).T
    else:
        return None

    data.set_index(pd.to_datetime(data.index), drop=True, inplace=True)
    for label in list(data.columns):
        data[label] = data[label].astype(float)
    return data


def fx_it(function, symbol, interval, apikey=None, **kargs):
    URL_BASE = "https://www.alphavantage.co/query"
    parametros = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        **kargs,
        "apikey": apikey,
    }

    r = requests.get(URL_BASE, params=parametros)
    try:
        js = r.json()[f"Technical Analysis: {function}"]
        df = pd.DataFrame.from_dict(js, orient="index")
        df = df.astype(float)
        df.index.name = "Date"
        df = df.sort_values("Date", ascending=True).round(3)
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        print(f"Exception: {e}")
        df = pd.DataFrame()
        print(r.json())
    except:
        df = pd.DataFrame()
        print(r.json())
    return df


def fx_get_exchanges(TOKEN):
    url = "https://finnhub.io/api/v1/forex/exchange"
    r = requests.get(url, params={"token": TOKEN})
    js = r.json()
    return js


def fx_exchange_symbols(exchange, TOKEN):
    url = "https://finnhub.io/api/v1/forex/symbol"
    p = {"token": TOKEN, "exchange": exchange}
    r = requests.get(url, params=p)
    js = r.json()
    return js


# TODO: Parametros por default
# https://polygon.io/docs/forex/getting-started
def fx_symbol_candles(forexTicker, multiplier, timespan, fromS, toS, apikey):
    """
    timespan's: minute, hour, day, week, month, quarter, year
    fromS, toS: need format %Y-%m-%d
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


def convert_to_timestamp(dateDT: str) -> datetime.timestamp:
    return int(dt.datetime.timestamp(dateDT)) * 1000


if __name__ == "__main__":
    from pprint import pprint

    load_dotenv()
    TOKEN = os.environ["TOKEN_AV"]
    # data = fx_price("FX_MONTHLY", "EUR", "USD", TOKEN)
    # macdext = fx_it(function="MACDEXT", symbol="EURUSD", interval="daily", series_type="close", fast_period=12, slow_period=26, signal_period=9, apikey=TOKEN)
    # pprint(data)

    TOKEN2 = os.environ["TOKEN_FH"]
    # pprint(fx_get_exchanges(TOKEN2))
    """['oanda', 'fxcm','forex.com', 'icmtrader', 'fxpro', 'pepperstoneuk', 'ic markets', 'fxpig', 'pepperstone']"""

    # pprint (fx_exchange_symbols('fxpro', TOKEN2))
    # OK

    #### pprint (fx_symbol_candles('fxpro', 'NZD/USD', 60, '2022-01-01', '2022-05-05',TOKEN2))

    TOKEN3 = os.environ["TOKEN_PG"]
    pprint(
        len(
            fx_symbol_candles("EURJPY", "1", "hour", "2018-01-01", "2022-10-29", TOKEN3)
        )
    )
