from kafka import KafkaConsumer, KafkaProducer
from time import sleep
from json import dumps
import json
import requests
import logging
import os

# Configurations and initialization
logging.basicConfig(filename='../logs/crawl.log', format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().setLevel(logging.INFO) 

def reportLog(msg, level):
    print(msg)
    if level == 'debug':
        logging.debug(msg)
    elif level == 'info':
        logging.info(msg)
    elif level == 'warn':
        logging.warn(msg)
    elif level == 'error':
        logging.error(msg)
    elif level == 'critical':
        logging.critical(msg)
    else:
        logging.fatal('Provided log level is not valid')
     

def getDataFromRest(base_url, api_key, symbol):
    function = "TIME_SERIES_DAILY"
    # API paramters
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)
    response_json = response.json()

    if 'Error Message' in response_json:
        logging.fatal(f"Error fetching data from Alpha Vantage: {response_json['Error Message']}")
        raise Exception("Error fetching data from Alpha Vantage:" + response_json['Error Message'])
    elif 'Note' in response_json:
        logging.fatal(f"API call frequency limit reached: {response_json['Note']}")
        raise Exception("API call frequency limit reached: " + response_json['Note'])
    elif 'Time Series (Daily)' not in response_json:
        logging.fatal(f"Unexpected response from Alpha Vantage: {response_json}")
        raise Exception("Unexpected response from Alpha Vantage: ", response_json)
    return response_json

if __name__ == '__main__':
    base_url = "https://www.alphavantage.co/query"
    symbol = "AAPL"
    api_key = os.environ.get('APIKEY')

    if api_key is None:
        raise ValueError("Environment variable 'APIKEY' not found")
    else:
        print("API Key Successfully connected")
        logging
    # Connect to Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
    # Send message toward topic
    future = producer.send('nasdaq_prices', value=getDataFromRest())

    # Block until the message is sent and get the metadata
    try:
        record_metadata = future.get(timeout=10)
        print(f"Message sent successfully to {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}")
        # Log the data
        log_msg = f"Symbol: {symbol}, Price: {price}"
        logging.info(log_msg)
    except Exception as e:
        error_msg = f"Error sending message: {e}"
        print(error_msg)
        logging.warn(error_msg)
    finally:
        # Close the producer to flush any remaining messages
        producer.close()
        logging.info("close kafka producer process")