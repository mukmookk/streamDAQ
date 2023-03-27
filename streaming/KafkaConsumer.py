mport pandas as pd
from kafka import KafkaConsumer

consumer = KafkaConsumer(
'nasdaq_prices',
bootstrap_servers=['127.0.0.1:9092'],
value_deserializer=lambda x : json.loads(x.decode('utf-8')))

print("Messages start streaming...")

for message in consumer:
    print(f"Received message: {message.value}")

print("Message streaming finished.")