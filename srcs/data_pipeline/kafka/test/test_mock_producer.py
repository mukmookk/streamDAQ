import pytest
from data_pipeline.kafka.streaming_producer import KafkaProducer
import json

@pytest.fixture(scope="module")
def kafka_producer():
    producer = KafkaProducer('kafka1', 9092)
    yield producer
    producer.flush()

@pytest.mark.parametrize("topic, data", [
    ('test-topic-1', {'key1': 'value1'}),
    ('test-topic-2', {'key2': 'value2'}),
    ('test-topic-3', {'key3': 'value3'}),
])
def test_kafka_producer(kafka_producer, topic, data):
    kafka_producer.produce_msg_from_function(data, topic)

