import pandas as pd
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'nasdaq_prices',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x : json.loads(x.decode('utf-8'))
)

# Poll the consumer to get assigned partitions
consumer.poll()

# Seek to the end of each assigned partition
for partition in consumer.assignment():
    consumer.seek_to_end(partition)

print("Messages start streaming...")

try:
    for message in consumer:
        print(f"Received message: {message.value}")
except:
    print("Message streaming finished.")

print("Message streaming finished.")