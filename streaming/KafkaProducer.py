import time
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json
import requests
import logging
import os

# Configurations and initialization
logging.basicConfig(filename='./logs/crawl.log', format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().setLevel(logging.INFO)

base_url = "https://www.alphavantage.co/query"
symbol = "AAPL"
api_key = os.environ.get('APIKEY')

def reportLog(msg, level):
    log_levels = {
        'debug': logging.debug,
        'info': logging.info,
        'warn': logging.warning, # Note: Use 'warning' instead of 'warn'
        'error': logging.error,
        'critical': logging.critical,
    }

    log_func = log_levels.get(level.lower())

    if log_func is not None:
        log_func(msg)
        print(msg)
    else:
        logging.fatal('Provided log level is not valid')
        print('Provided log level is not valid')
     

def getDataFromRest(function="TIME_SERIES_DAILY_ADJUSTED", symbol="AAPL"):
    # API paramters
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)
    response_json = response.json()

    if 'Error Message' in response_json:
        reportLog(f"Error fetching data from Alpha Vantage: {response_json['Error Message']}", "error")
        raise Exception("Error fetching data from Alpha Vantage:" + response_json['Error Message'])
    elif 'Note' in response_json:
        reportLog(f"API call frequency limit reached: {response_json['Note']}", "error")
        raise Exception("API call frequency limit reached: " + response_json['Note'])
    elif 'Time Series (Daily)' not in response_json:
        reportLog(f"Unexpected response from Alpha Vantage: {response_json}", "error")
        raise Exception("Unexpected response from Alpha Vantage: ", response_json)
    return response_json

def getLatestPrice(response_json):
    # Get latest price
    latest_price_idx = list(response_json['Time Series (Daily)'])[0]
    latest_price = response_json['Time Series (Daily)'][latest_price_idx]['4. close']
    latest_price_timestamp = response_json['Time Series (Daily)'][latest_price_idx]

    # Create dictionary with index, timestamp, and latest price
    data = {
        "date": latest_price_idx,
        "symbol": symbol,
        "timestamp": latest_price_timestamp,
        "latest_price": latest_price,
    }

    print(data)
    # Serialize dictionary to JSON and return
    return json.dumps(data)

def main():
    if api_key is None:
        reportLog("Environment variable 'APIKEY' not found", "error")
        raise ValueError("Environment variable 'APIKEY' not found")
    else:
        reportLog("API Key Successfully connected", 'info')

    response_json = getDataFromRest()
    latest_price = getLatestPrice(response_json)
    # Connect to Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
                        
    # Send message toward topic
    future = producer.send('nasdaq_prices', 
                           value=response_json)

    future = producer.send('lastest_price', 
                           value=getLatestPrice(response_json))
    
    # time to wait for api limit (5 calls per minute)
    start_time = time.time()
    time_waited = 0
    
    # # Block until the message is sent and get the metadata
    try:
        record_metadata = future.get(timeout=10)
        reportLog(f"Message sent successfully to {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}", 'info')
        # Log the data
        reportLog(f"Symbol: {symbol} successfully reported", 'info')
    except Exception as e:
        error_msg = f"Error sending message: {e}"
        reportLog(error_msg, 'error')
    finally:
        # Close the producer to flush any remaining messages
        producer.close()
        reportLog("close kafka producer process", 'info')
    
    while time.time() - start_time < 12:
        time_waited += 1
        time.sleep(1)
    reportLog("Waited for {} seconds".format(time_waited), 'info')

if __name__ == '__main__':
    while (1):
        main()