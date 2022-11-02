# TODO: finnhub documentation

import requests


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


# def fx_symbol_candles(exchange, symbol, interval, fromS, toS, TOKEN):
# NECESITA SERVICIO PREMIUM PARA USAR EL ENDPOINT
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
