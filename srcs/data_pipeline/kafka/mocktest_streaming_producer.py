import pytest
from unittest.mock import Mock
from kafka_producer import KafkaProducer
from confluent_kafka import Producer

@pytest.fixture
def mock_producer():
    return Mock(spec=Producer)

@pytest.fixture
def kafka_producer(mock_producer):
    return KafkaProducer(producer=mock_producer)

def test_produce(kafka_producer, mock_producer):
    kafka_producer.produce('sameple-topic', 'test_message')
    mock_producer.produce.assert_called_once_with('test_topic', 'test_message'.encode('utf-8'), callback=kafka_producer.delivery_report)
    mock_producer.poll.assert_called_once_with(0)

def test_produce_msg_from_file(kafka_producer, mock_producer, mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data='[{"test": "data"}]'))
    kafka_producer.produce_msg_from_file('test_file_path', 'test_topic')
    mock_producer.produce.assert_called_once_with('test_topic', '{"test": "data"}'.encode('utf-8'), callback=kafka_producer.delivery_report)
    mock_producer.flush.assert_called_once()

# Add more tests for the remaining methods
