import os
from dotenv import load_dotenv  # remember: pip install python-dotenv
import requests
import pandas as pd


def fx_price(function, from_symbol, to_symbol, api_key, output_size="full"):
    """API SERVICE OF ALPHA VANTAGE

    Keyword arguments:
    function = FX_DAILY, FX_WEEKLY, FX_MONTHLY
    from_symbol: first asset
    to_symbol: second asset
    api_key: personal TOKEN
    output_size: "full", "compact", 
    Return: pandas.DataFrame
    """

    function = function
    from_symbol = from_symbol
    to_symbol = to_symbol
    api_key = api_key

    URL_BASE = "https://www.alphavantage.co/"

    URL = URL_BASE + "query?function=" + function
    URL += "&from_symbol=" + from_symbol
    URL += "&to_symbol=" + to_symbol
    URL += "&outputsize=" + output_size
    URL += "&apikey=" + api_key

    r = requests.get(URL)
    data = r.json()

    # Acá podría caber un context manager

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


if __name__ == "__main__":
    from pprint import pprint

    load_dotenv()
    TOKEN = os.environ["TOKEN_AV"]
    data = alpha_vantage_fx_api("FX_MONTHLY", "EUR", "USD", TOKEN)
    pprint(data)
