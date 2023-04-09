from alpha_vantage.timeseries import TimeSeries
import time
import requests
import json
import csv
from streaming.kafka.utils.utils import reportLog
from kafka import KafkaProducer

bootstrap_servers = ['localhost:9092']
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, 
                         value_serializer=lambda v: json.dumps(v).decode('utf-8'))

def earnings(key, ticker):
    """
    key = API key from Alpha Vantage
    ticker = ticker to be used
    
    return dataframe of earnings data
    """

    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol={}&interval=1min&apikey={}'.format(ticker, key)
    
    # use requests to get the data
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        earnings = list(cr)
        
        start_time = time.time()

        if earnings:
            # select the data from the dictionary
            reportLog("Successfully retrieved data for {}".format(ticker), "info")
        else:
            reportLog("No data for this ticker", "WARN")
            return "No data for this ticker"

        time_waited = 0
        while time.time() - start_time < 12:
            time_waited += 1
            time.sleep(1)
            
        return earnings

