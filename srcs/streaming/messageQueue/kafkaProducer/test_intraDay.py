import json
import os
import time

import pytest
import requests
from kafka import KafkaProducer
from json import dumps

from app import timeSeriesIntraDay

base_url = "https://www.alphavantage.co/query"
symbol = os.environ.get('SYMBOL')
api_key = os.environ.get('APIKEY')

@pytest.fixture
def mock_api_response():
    return {
        "Meta Data": {
            "1. Information": "Intraday (5min) open, high, low, close prices and volume",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2022-01-01 23:55:00",
            "4. Interval": "5min",
            "5. Output Size": "Compact",
            "6. Time Zone": "US/Eastern"
        },
        "Time Series (5min)": {
            "2022-01-01 23:55:00": {
                "1. open": "179.2200",
                "2. high": "179.2200",
                "3. low": "179.2200",
                "4. close": "179.2200",
                "5. volume": "200"
            }
        }
    }

@pytest.fixture
def producer():
    producer = KafkaProducer(bootstrap_servers=[bootstrap_servers],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    yield producer
    producer.close()

def test_timeSeriesIntraDay(monkeypatch, mock_api_response, producer):
    monkeypatch.setattr(requests, "get", lambda url, params: MockResponse(mock_api_response))
    
    response_json = timeSeriesIntraDay()
    
    future = producer.send('nasdaq_prices', value=response_json)
    record_metadata = future.get(timeout=10)

    assert record_metadata.topic == "nasdaq_prices"
    assert record_metadata.partition is not None
    assert record_metadata.offset is not None
    assert response_json == mock_api_response

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data