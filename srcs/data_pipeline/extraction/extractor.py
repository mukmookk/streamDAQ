'''
Class definition for extractor
'''

from datetime import datetime
import logging
import json
import sys
import re
import requests
from bs4 import BeautifulSoup

class Extractor:
    '''
    super class for extractor
    '''
    def __init__(self, ticker):
        self.ticker = ticker

class StreamingDataExtractor(Extractor):
    '''
    class for streaming data extractor
    '''
    def __init__(self, ticker, url):
        super().__init__(ticker)
        self.url = url
        self.response = self.get_response()
        self.soup = self.get_soup()
        self.last_update_time = None
        self.retries = 10

    def get_response(self):
        '''
        get response from url
        '''
        try:
            response = requests.get(self.url, timeout=60)
            if response is None:
                logging.error('get_response: response is None')
                raise ValueError('get_response: response is None')
        except Exception as exception:
            logging.error('get_response: %s', exception)
            raise ValueError('get_soup: soup is None') from exception
        return response

    def get_soup(self):
        '''
        get soup from response
        '''
        soup = BeautifulSoup(self.response.text, 'html.parser')
        if soup is None:
            logging.error('get_soup: soup is None')
            raise ValueError('get_soup: soup is None')
        return soup

    def parse_for_yahoofinace(self, raw_string):
        '''
        parse raw string from yahoo finance
        '''
        pattern = r'[+\s()%A-Za-z]'
        string = raw_string.strip()
        lst = re.split(pattern, string)
        lst = [x for x in lst if x != '']
        price, change, change_percent, trade_time = lst[0:4]
        return {
            'price': price,
            'chagne': change,
            'change_percent': change_percent,
            'last_trade_time': trade_time
        }

    def fetch_realtime_data(self):
        '''
        fetch real time data from yahoo finance
        '''
        tries = 0
        while tries < self.retries:
            if tries == self.retries:
                logging.error('fetch_realtime_data: No update')
                logging.error('fetch_realtime_data: last_update_time: %s', self.last_update_time)
                sys.exit(0)
            price_element = self.soup.find('div', {'class': 'D(ib) Mend(20px)'})
            if price_element is None:
                tries += 1
                logging.error('fetch_realtime_data: price_element is None. Retry %s', tries)
            else:
                self.last_update_time = datetime.now().strftime('%H:%M:%S')
                break
        parsed_data = self.parse_for_yahoofinace(price_element.text)
        json_data = json.dumps(parsed_data)
        return json_data
   