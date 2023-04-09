from kafka import KafkaProducer
import logging
import requests
import json

# Set up logging to write to file
logging.basicConfig(filename='../logs/aapl_price.log', format='%(asctime)s %(levelname)s %(message)s')

# Set up ticker and URL
symbol = "AAPL"
url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks"

# Generate kafka producer to generate 
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Get data from API endpoint
response = requests.get(url)
data = response.json()
price = data['data']['primaryData']['lastSalePrice']

# Log the data
log_msg = f"Symbol: {symbol}, Price: {price}"
logging.info(log_msg)

# Send price data into topic 'nasdaq-prices' and make it JSON encoded ddat type
producer.send('nasdaq-prices', json.dumps({'symbol': symbol, 'price': price}).encode())
