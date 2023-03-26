from kafka import KafkaConsumer, KafkaProducer
from time import sleep
from json import dumps
import json
import logging

# Configurations and initialization
logging.basicConfig(filename='../logs/crawl.log', format='%(asctime)s %(levelname)s %(message)s')

symbol = "AAPL"
price = 0

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