import yfinance as yf
import json


class Extractor:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)
        self.metadata = {
            'currency': '',
            'symbol': '',
            'exchangeName': '',
            'instrumentType': '',
            'firstTradeDate': '',
            'regularMarketTime': '',
            'gmtoffset': '',
            'timezone': '',
            'exchangeTimezoneName': '',
            'regularMarketPrice': '',
            'chartPreviousClose': '',
            'priceHint': '',
            'currentTradingPeriod': {
                'pre': {'end': '', 'start': ''},
                'regular': {'end': '', 'start': ''},
                'post': {'end': '', 'start': ''}
            },
            'dataGranularity': '',
            'range': '',
            'validRanges': []
        }

    def setTickerHistInfo(self):
        self.ticker.history(period='max')
        history_metadata = self.ticker.history_metadata
        self.metadata = {
            'currency': history_metadata['currency'],
            'symbol': history_metadata['symbol'],
            'exchangeName': history_metadata['exchangeName'],
            'instrumentType': history_metadata['instrumentType'],
            'firstTradeDate': history_metadata['firstTradeDate'],
            'regularMarketTime': history_metadata['regularMarketTime'],
            'gmtoffset': history_metadata['gmtoffset'],
            'timezone': history_metadata['timezone'],
            'exchangeTimezoneName': history_metadata['exchangeTimezoneName'],
            'regularMarketPrice': history_metadata['regularMarketPrice'],
            'chartPreviousClose': history_metadata['chartPreviousClose'],
            'priceHint': history_metadata['priceHint'],
            'currentTradingPeriod': {
                'pre': {
                    'end': history_metadata['currentTradingPeriod']['pre']['end'],
                    'start': history_metadata['currentTradingPeriod']['pre']['start']
                },
                'regular': {
                    'end': history_metadata['currentTradingPeriod']['regular']['end'],
                    'start': history_metadata['currentTradingPeriod']['regular']['start']
                },
                'post': {
                    'end': history_metadata['currentTradingPeriod']['post']['end'],
                    'start': history_metadata['currentTradingPeriod']['post']['start']
                }
            },
            'dataGranularity': history_metadata['dataGranularity'],
            'range': history_metadata['range'],
            'validRanges': history_metadata['validRanges']
        }

    # def extract(self):
    #     self.data = yf.Ticker(self.ticker).info

    # def save(self, path):
    #     with open(path, 'w') as f:
    #         json.dump(self.data, f)
