from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import re

class Market:
    """
    Market class
    """
    def __init__(self):
        self.status = None

class Stock:
    """
    Stock class
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.price = None
        self.change = None
        self.percent_change = None
        self.last_trade_time = None
        
        self.price_related = ['price', 
                         'change', 
                         'percent_change']

    
    def updateRealTimeData(self, *args):
        last_time = datetime.now().strftime('%H:%M:%S')
                
        if self.last_trade_time == last_time:
            print("No update")
        
        if self.last_trade_time != last_time:
            self.last_trade_time = last_time
            for i, var in enumerate(self.price_related):
                setattr(self, var, args[i])
            print("Update")
        

    def parsing(self, rawstring):
        pattern = r'[+\s()%A-Za-z]'
        lst = re.split(pattern, rawstring)
        lst = [x for x in lst if x != '']
        price, change, percent_change = map(float, lst[0:3])
        last_trade_time = lst[3]
        self.updateRealTimeData(price, change, percent_change, last_trade_time)
        print(self.price, self.change, self.percent_change, self.last_trade_time)
    
def main():
    url = 'https://finance.yahoo.com/quote/AAPL'
    response = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('div', {'class': 'D(ib) Mend(20px)'})
    price_text = price_element.text.strip()

    aapl = Stock("AAPL")
    aapl.parsing(price_text)
    print(price_text.split())

if __name__ == "__main__":
    main()
    


