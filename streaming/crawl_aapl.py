from kafka import KafkaProducer
import requests
import json

symbol = "AAPL"
url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks"

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

response = requests.get(url)
data = response.json()

price = data['data']['primaryData']['lastSalePrice']

producer.send('nasdaq-prices', json.dumps({'symbol': symbol, 'price': price}).encode())
