import pytest
from data_pipeline.kafka.streaming_producer import KafkaProducer
import json

def test_kafka_producer():
    # Instantiate the producer with the broker's hostname and port
    kafka_producer = KafkaProducer('kafka1', 9092)
    topic = 'test-topic'
    data = {'test': 'kafka-communication-test'}
    kafka_producer.produce_msg_from_function(data, topic, dumped=False)
    kafka_producer.flush()

test_kafka_producer()