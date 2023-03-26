from kafka import KafkaConsumer, KafkaProducer
from time import sleep
from json import dumps
import json
import logging

# Configurations
logging.basicConfig(filename='../logs/crawl.log', format='%(asctime)s %(levelname)s %(message)s')

# Connect to Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# Send message toward topic
future = producer.send('nasdaq_prices', value={"hello" : "world"})

# Block until the message is sent and get the metadata
try:
    record_metadata = future.get(timeout=10)
    print(f"Message sent successfully to {record_metadata.topic} "
          f"partition {record_metadata.partition} "
          f"offset {record_metadata.offset}")
except Exception as e:
    print(f"Error sending message: {e}")
finally:
    # Close the producer to flush any remaining messages
    producer.close()