'''
Class definition for extractor
'''

from datetime import datetime
import logging
import json
import sys
import re
import requests
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
    
class Extractor:
    """
    common class for extractor
    """
    def __init__(self, ticker):
        """_summary_
        init method of HistoricalDataExtractor
        Args:
            ticker (str): ticker of stock
            header (dict): header for request
        """
        self.ticker = ticker
        self.header = {
            "User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/94.0.4606.71 Safari/537.36"
        }
                
    def get_response(self, role):
        """_summary_
        get response from url
        Args:
            role (str): one of ['realtime', 'profile', 'financials', 'statistics', 'historical']

        Raises:
            ValueError: if response is None
            ValueError: if soup is None

        Returns:
            response: response from url
        """
        url = self.get_target_url(role)
        try:
            response = requests.get(url, headers=self.header, timeout=60)
            if response is None:
                logging.error('get_response: response is None')
                raise ValueError('get_response: response is None')
        except Exception as exception:
            logging.error('get_response: %s', exception)
            raise ValueError('get_soup: soup is None') from exception
        return response
    
    def get_soup(self, role):
        """_summary_
        get soup from response
        Args:
            role (_type_): ['realtime', 'profile', 'financials', 'statistics', 'historical']

        Raises:
            ValueError: if soup is None

        Returns:
            _type_: _description_
        """
        response = self.get_response(role)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup is None:
            logging.error('get_soup: soup is None')
            raise ValueError('get_soup: soup is None')
        return soup

    def get_target_url(self, role):
        """_summary_
        return url for different roles
        Args:
            role (str): ['realtime', 'profile', 'financials', 'statistics', 'historical']

        Returns:
            str: url
        """
        if not role in ['realtime', 'profile', 'financials', 'statistics', 'historical']:
            return False
        ticker = self.ticker
        if role == 'realtime':
            url = 'https://finance.yahoo.com/quote/' + ticker
        elif role == 'financials':
            url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
        elif role == 'statistics':
            url = 'https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
        elif role == 'historical':
            url = 'https://finance.yahoo.com/quote/' + ticker + '/history?p=' + ticker

        return url
    
    def save_json(self, output_file, json_data):
        """_summary_
        save json data to output file
        Args:
            output_file (str): output file
            json_data (json): json data
        """
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file)
    
    @contextmanager
    def chrome_driver(self, url):
        driver = None
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            yield driver
        finally:
            if driver:
                driver.quit()
    
    def click_button_selenuim_driver(self, url, target_element):
        with self.chrome_driver(url) as driver:
            try:
                button = driver.find_element(By.CSS_SELECTOR, target_element)
                button.click()
            except NoSuchElementException:
                logging.error('click_button_selenuim_driver: NoSuchElementException')
                exit(1)
            except TimeoutException:
                logging.error('click_button_selenuim_driver: TimeoutException')
                exit(1)
    
    def validate_selenuim_selector(self, url, button):
        with self.chrome_driver(url) as driver:
            try:
                button = driver.find_element(By.CSS_SELECTOR, button)
                button.click()
                print("Button found")
            except NoSuchElementException:
                print("Button not found")
    
class StreamingDataExtractor(Extractor):
    """_summary_
    init StreamingDataExtractor
    Args:
        Extractor (class): super class of StreamingDataExtractor
    """
    def __init__(self, ticker):
        """_summary_
        init method of StreamingDataExtractor
        Args:
            ticker (str): ticker of stock
        """
        super().__init__(ticker)
        self.retries = 10
        self.response = None
        self.last_update_time = None

    def parse_for_realtime_data(self, raw_string):
        """_summary_
        parse raw string from yahoo finance
        Args:
            raw_string (str): raw string from yahoo finance

        Returns:
            dict: parsed from raw string
        """
        pattern = r'[+\s()%A-Za-z]'
        string = raw_string.strip()
        lst = re.split(pattern, string)
        lst = [x for x in lst if x != '']
        price, change, change_percent, trade_time = lst[0:4]
        msg = 'Market Open'
        if trade_time == ':':
            trade_time = datetime.now().strftime('04:00')
            msg = 'Market Closed'        
        return {
            'price': price,
            'change': change,
            'change_percent': change_percent,
            'last_trade_time': trade_time,
            'msg': msg
        }

    def fetch_realtime_data(self):
        """_summary_
        Stream data from yahoo finance, direct to kafka producer
        Raises:
            ValueError: if soup is None

        Returns:
            json: realtime data in json format
        """
        tries = 0
        while tries < self.retries:
            if tries == self.retries:
                logging.error('fetch_realtime_data: No update')
                logging.error('fetch_realtime_data: last_update_time: %s', self.last_update_time)
                sys.exit(0)
            soup = self.get_soup('realtime')
            price_element = soup.find('div', class_='D(ib) Mend(20px)')
            if price_element is None:
                tries += 1
                logging.error('fetch_realtime_data: price_element is None. Retry %s', tries)
            else:
                self.last_update_time = datetime.now().strftime('%H:%M:%S')
                break
        parsed_data = self.parse_for_realtime_data(price_element.text)
        json_data = json.dumps(parsed_data)
        
        # ** 추후 kafka producer와 연결 **
        return json_data        

class HistoricalDataExtractor(Extractor):
    """_summary_
    
    Args:
        Extractor (_type_): super class of HistoricalDataExtractor
    """
    def __init__(self, ticker):
        """_summary_
        init method of HistoricalDataExtractor
        Args:
            ticker (str): ticker of stock
        """
        super().__init__(ticker)
        
    def fetch_historical_data(self, output_path, duration='1sec'):
        """_summary_
        fetch historical data from yahoo finance, save to output file
        Returns:
            json: historical data in json format
        """
        soup = self.get_soup('historical')
        price_element = soup.find('table', {'class': 'W(100%) M(0)'})
        history_data = []
        # button_element = 'button.Py(5px).W(45px).Fz(s).C($tertiaryColor).Cur(p).Bd.Bdc($seperatorColor).Bgc($lv4BgColor).Bdc($linkColor):h.Bdrs(3px)[data-value="MAX"]'
        # self.click_button_selenuim_driver(self.get_target_url('historical'), button_element)
        while True:
            row = price_element.find_next('tr', {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
            if row is None:
                break
            date = row.find_next('td', {'class': 'Py(10px) Ta(start) Pend(10px)'})
            open = date.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            high = open.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            low = high.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            close = low.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            adjclose = close.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            volume = adjclose.find_next('td', {'class': 'Py(10px) Pstart(10px)'})
            
            input_format = '%b %d, %Y'
            output_format = '%Y-%m-%d'
            date = datetime.strptime(date.text, input_format).strftime(output_format)
            parsed_item = {
                "date": date,
                "open": open.text,
                "high": high.text,
                "low": low.text,
                "close": close.text,
                "adjclose": adjclose.text,
                "volume": volume.text
            }
            history_data.append(parsed_item)
            price_element = row
        
        self.save_json(output_path, history_data)
        logging.info('fetch_historical_data: successfully saved historical data to %s', output_path)
        return "successfully saved historical data to " + output_path
        

   