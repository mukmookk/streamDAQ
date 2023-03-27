import pandas as pd
from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json

consumer = KafkaConsumer(
        'nasdaq_prices',
        bootstrap_servers=['127.0.0.1:9092'],
        value_deserializer=lambda x : loads(x.decode('utf-8')))

print("Message Starts")

for c in consumer:
    print(c, c.value)

print("Message Ends")
