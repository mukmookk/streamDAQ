import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
import time

def test_kafka_consumer():
        producer = KafkaProducer(bootstrap_servers=[bootstrap_servers],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    # Send a test message to the nasdaq_prices topic
    test_message = {'test_key': 'test_value'}
    producer.send('nasdaq_prices', value=test_message)

    consumer = KafkaConsumer('nasdaq_prices', bootstrap_servers=[bootstrap_servers],
                             auto_offset_reset='latest',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Poll the consumer to get assigned partitions
    consumer.poll()

    # Seek to the end of each assigned partition
    for partition in consumer.assignment():
        consumer.seek_to_end(partition)

    # Wait for the message to be received by the consumer
    time.sleep(5)

    # Check that the message is received
    received_message = None
    for message in consumer:
        if message.value == test_message:
            received_message = message.value
            break

    assert received_message == test_message