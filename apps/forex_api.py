"""https://www.alphavantage.co/documentation/"""
#TODO: finnhub documentation

import os
from dotenv import load_dotenv  # remember: pip install python-dotenv
import requests
import pandas as pd
from datetime import datetime


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

    parametros = {'function': function, 'from_symbol': from_symbol, 'to_symbol':to_symbol,'outputsize':outputsize, 'apikey': api_key}

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
    parametros = {'function':function, 'symbol':symbol, 'interval':interval,
    **kargs,
    'apikey':apikey
    }

    r = requests.get(URL_BASE, params=parametros)
    try:
        js = r.json()[f"Technical Analysis: {function}"]
        df = pd.DataFrame.from_dict(js, orient='index')
        df = df.astype(float)
        df.index.name = "Date"
        df = df.sort_values('Date', ascending=True).round(3)
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        print (f"Exception: {e}")
        df = pd.DataFrame()
        print (r.json())
    except:
        df = pd.DataFrame()
        print (r.json())
    return df



def fx_get_exchanges(TOKEN):
    url = "https://finnhub.io/api/v1/forex/exchange"
    r = requests.get(url, params={'token': TOKEN})
    js = r.json()
    return js

def fx_exchange_symbols(exchange, TOKEN):
    url = "https://finnhub.io/api/v1/forex/symbol"
    p = {'token': TOKEN, 'exchange': exchange}
    r = requests.get(url, params=p)
    js = r.json()
    return js

# def fx_symbol_candles(exchange, symbol, interval, fromS, toS, TOKEN):
# NECESITA SERVICIO PREMIUN PARA USAR EL ENDPOINT
#     s = exchange + ':' + symbol
#     fromDT = datetime.strptime(fromS, '%Y-%m-%d')
#     fromTS = int(datetime.timestamp(fromDT))
#     toDT = datetime.strptime(toS, '%Y-%m-%d')
#     toTS = int(datetime.timestamp(toDT))

#     url = "https://finnhub.io/api/v1/forex/candle"
#     p = {'token':TOKEN, 'symbol': s, 'resolution':interval, 'from':fromTS, 'to':toTS}
#     r = requests.get(url, params=p)
#     js = r.json()

#     # df = pd.DataFrame(js)
#     return js


if __name__ == "__main__":
    from pprint import pprint

    load_dotenv()
    TOKEN = os.environ["TOKEN_AV"]
    # data = fx_price("FX_MONTHLY", "EUR", "USD", TOKEN)
    # macdext = fx_it(function="MACDEXT", symbol="EURUSD", interval="daily", series_type="close", fast_period=12, slow_period=26, signal_period=9, apikey=TOKEN)
    # pprint(data)

    TOKEN2 = os.environ["TOKEN_FH"]
    # pprint(fx_get_exchanges(TOKEN2))
    """['oanda', 'fxcm','forex.com', 'icmtrader', 'fxpro', 'pepperstoneuk', 'ic markets', 'fxpig', 'pepperstone']""";

    # pprint (fx_exchange_symbols('fxpro', TOKEN2)) 
    # OK

    pprint (fx_symbol_candles('fxpro', 'NZD/USD', 60, '2022-01-01', '2022-05-05',TOKEN2))
