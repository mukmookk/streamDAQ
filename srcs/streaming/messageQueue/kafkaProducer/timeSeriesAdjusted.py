import time
import config
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json
import requests
import os

base_url = "https://www.alphavantage.co/query"
symbol = "AAPL"
api_key = os.environ.get('APIKEY')

def getTimeSeriesDailyAdjusted(function="TIME_SERIES_DAILY_ADJUSTED", symbol="AAPL"):
    """
    function = function to be used
    symbol = ticker to be used
    """
    # API paramters
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)
    response_json = response.json()

    if 'Error Message' in response_json:
        config.reportlog(f"Error fetching data from Alpha Vantage: {response_json['Error Message']}", "error")
        raise Exception("Error fetching data from Alpha Vantage:" + response_json['Error Message'])
    elif 'Note' in response_json:
        config.reportlog(f"API call frequency limit reached: {response_json['Note']}", "error")
        raise Exception("API call frequency limit reached: " + response_json['Note'])
    elif 'Time Series (Daily)' not in response_json:
        config.reportlog(f"Unexpected response from Alpha Vantage: {response_json}", "error")
        raise Exception("Unexpected response from Alpha Vantage: ", response_json)
    return response_json

def getLatestPrice(response_json, symbol):
    # Get latest price
    latest_price_idx = list(response_json['Time Series (Daily)'])[0]
    latest_price = response_json['Time Series (Daily)'][latest_price_idx]['4. close']
    latest_price_timestamp = response_json['Time Series (Daily)'][latest_price_idx]

    # Create dictionary with index, timestamp, and latest price
    data = {
        "date": latest_price_idx,
        "symbol": symbol,
        "1. open": latest_price_timestamp["1. open"],
        "2. high": latest_price_timestamp["2. high"],
        "3. low": latest_price_timestamp["3. low"],
        "4. close": latest_price,
        "5. adjusted close": latest_price_timestamp["5. adjusted close"],
        "6. volume": latest_price_timestamp["6. volume"],
        "7. dividend amount": latest_price_timestamp["7. dividend amount"],
        "8. split coefficient": latest_price_timestamp["8. split coefficient"]
    }
    # Serialize dictionary to JSON and return
    return json.dumps(data)

def main():
    if api_key is None:
        config.reportlog("Environment variable 'APIKEY' not found", "error")
        raise ValueError("Environment variable 'APIKEY' not found")
    else:
        config.reportlog("API Key Successfully connected", 'info')

    response_json = getTimeSeriesDailyAdjusted()
    latest_price = getLatestPrice(response_json, "AAPL")
    # Connect to Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
                        
    # Send message toward topic
    future = producer.send('nasdaq_prices', 
                           value=response_json)

    future = producer.send('lastest_price', 
                           value=latest_price)
    
    # time to wait for api limit (5 calls per minute)
    start_time = time.time()
    time_waited = 0
    
    # # Block until the message is sent and get the metadata
    try:
        record_metadata = future.get(timeout=10)
        config.reportlog(f"Message sent successfully to {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}", 'info')
        # Log the data
        config.reportlog(f"Symbol: {symbol} successfully reported", 'info')
    except Exception as e:
        error_msg = f"Error sending message: {e}"
        config.reportlog(error_msg, 'error')
    finally:
        # Close the producer to flush any remaining messages
        producer.close()
        config.reportlog("close kafka producer process", 'info')
    
    while time.time() - start_time < 12:
        time_waited += 1
        time.sleep(1)
    config.reportlog("Waited for {} seconds".format(time_waited), 'info')

if __name__ == '__main__':
    while (1):
        main()