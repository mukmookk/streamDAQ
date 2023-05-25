import requests
import json
import utils
import os

def searchSymbol(_keywords, _apiKey):
    """
    _keywords = keywords to be used
    _apikey = API key from Alpha Vantage
    """
    url = "https://www.alphavantage.co/query"
    function = "SYMBOL_SEARCH"
    keywords = _keywords
    if _apiKey is None:
        apiKey = os.environ.get('APIKEY')
        if apiKey is None:
            raise Exception("No API key provided.")
    else:
        apikey = _apiKey
    
    params = {
        "function": function,
        "keywords": keywords,
        "apikey": apikey
    }
    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        utils.reportlog(f"Error fetching data from Alpha Vantage: {e}", "error")
        raise SystemExit(e)

    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        utils.reportlog(f"Error decoding JSON: {e}", "error")
        raise SystemExit(e)

    if "bestMatches" in data:
        for match in data["bestMatches"]:
            symbol = match["1. symbol"]
            name = match["2. name"]
            utils.reportlog(f"Found ticker: {symbol} - {name}", "info")
    else:
        utils.reportLog("No matching tickers found.", "info")

def marketStatus(apikey):
    url = "https://www.alphavantage.co/query"
    function = "MARKET_STATUS"
    params = {
        "function": function,
        "apikey": apikey
    }
    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        utils.reportlog(f"Error fetching data from Alpha Vantage: {e}", "error")
        raise SystemExit(e)

    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        utils.reportlog(f"Error decoding JSON: {e}", "error")
        raise SystemExit(e)

    if "Global Quote" in data:
        status = data["Global Quote"]["09:30:00"]
        if status == "0.0000":
            utils.reportlog("Market is closed.", "info")
        else:
            utils.reportlog("Market is open.", "info")
    else:
        utils.reportlog("Error fetching market status.", "error")