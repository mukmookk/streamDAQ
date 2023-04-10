import json
from unittest import mock

import pytest
import requests

from main import timeSeriesDailyAdjusted

def test_timeSeriesDailyAdjusted_returns_dict():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'Time Series (Daily)': {'2021-01-01': {}}}

        result = timeSeriesDailyAdjusted(symbol='AAPL')

        assert isinstance(result, dict)


def test_timeSeriesDailyAdjusted_with_error():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'Error Message': 'Test Error Message'}

        with pytest.raises(Exception, match='Error fetching data from Alpha Vantage: Test Error Message'):
            timeSeriesDailyAdjusted(symbol='AAPL')


def test_timeSeriesDailyAdjusted_with_note():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'Note': 'Test Note'}

        with pytest.raises(Exception, match='API call frequency limit reached: Test Note'):
            timeSeriesDailyAdjusted(symbol='AAPL')


def test_timeSeriesDailyAdjusted_with_unexpected_response():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {}

        with pytest.raises(Exception, match='Unexpected response from Alpha Vantage: {}'):
            timeSeriesDailyAdjusted(symbol='AAPL')