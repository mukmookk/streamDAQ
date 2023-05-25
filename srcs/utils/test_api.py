import requests
import json
from unittest.mock import patch, Mock
import os

def test_searchSymbol():
    _keywords = "AAPL"
    _apiKey = "dummyapikey"
    mock_response = {
        "bestMatches": [
            {
                "1. symbol": "AAPL",
                "2. name": "Apple Inc.",
            }
        ]
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response
        searchSymbol(_keywords, _apiKey)
        mock_get.assert_called_with(
            "https://www.alphavantage.co/query",
            params={
                "function": "SYMBOL_SEARCH",
                "keywords": _keywords,
                "apikey": _apiKey
            }
        )

def test_marketStatus():
    apikey = "dummyapikey"
    mock_response = {
        "Global Quote": {
            "09:30:00": "1.0000"
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response
        marketStatus(apikey)
        mock_get.assert_called_with(
            "https://www.alphavantage.co/query",
            params={
                "function": "MARKET_STATUS",
                "apikey": apikey
            }
        )
