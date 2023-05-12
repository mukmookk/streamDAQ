import pytest
from unittest.mock import MagicMock
from data_pipeline.extraction.extractor import Extractor


@pytest.fixture
def extractor():
    ticker_mock = MagicMock()
    ticker_mock.history_metadata = {
        'currency': 'USD',
        'symbol': 'MSFT',
        'exchangeName': 'NMS',
        'instrumentType': 'EQUITY',
        'firstTradeDate': '2023-05-12',
        'regularMarketTime': '2023-05-12',
        'gmtoffset': -14400,
        'timezone': 'EDT',
        'exchangeTimezoneName': 'America/New_York',
        'regularMarketPrice': 310.11,
        'chartPreviousClose': 282.83,
        'priceHint': 2,
        'currentTradingPeriod': {
            'pre': {'end': '2023-05-12', 'start': '2023-05-12'},
            'regular': {'end': '2023-05-12', 'start': '2023-05-12'},
            'post': {'end': '2023-05-12', 'start': '2023-05-12'}
        },
        'dataGranularity': '1d',
        'range': '1mo',
        'validRanges': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    }

    ticker_mock.history.return_value = None

    extractor = Extractor('MSFT')
    extractor.ticker = ticker_mock

    return extractor


class TestExtractor:
    def test_setTickerHistInfo(self, extractor):
        extractor.setTickerHistInfo()

        assert extractor.metadata['currency'] == 'USD'
        assert extractor.metadata['symbol'] == 'MSFT'
        assert extractor.metadata['exchangeName'] == 'NMS'
        assert extractor.metadata['instrumentType'] == 'EQUITY'
        assert extractor.metadata['firstTradeDate'] == '2023-05-12'
        assert extractor.metadata['regularMarketTime'] == '2023-05-12'
        assert extractor.metadata['gmtoffset'] == -14400
        assert extractor.metadata['timezone'] == 'EDT'
        assert extractor.metadata['exchangeTimezoneName'] == 'America/New_York'
        assert extractor.metadata['regularMarketPrice'] == 310.11
        assert extractor.metadata['chartPreviousClose'] == 282.83
        assert extractor.metadata['priceHint'] == 2
        assert extractor.metadata['currentTradingPeriod']['pre']['end'] == '2023-05-12'
        assert extractor.metadata['currentTradingPeriod']['pre']['start'] == '2023-05-12'
        assert extractor.metadata['currentTradingPeriod']['regular']['end'] == '2023-05-12'
        assert extractor.metadata['currentTradingPeriod']['regular']['start'] == '2023-05-12'
        assert extractor.metadata['currentTradingPeriod']['post']['end'] == '2023-05-12'
        assert extractor.metadata['currentTradingPeriod']['post']['start'] == '2023-05-12'
        assert extractor.metadata['dataGranularity'] == '1d'
        assert extractor.metadata['range'] == '1mo'
        assert extractor.metadata['validRanges'] == [
            '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
