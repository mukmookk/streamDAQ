import logging
import json
import sys
import re
import argparse
import data_pipeline.extraction.extractor as extractor
from data_pipeline.kafka.producer import KafkaProducer

def validate_ticker(ticker):
    # Regex pattern to match ticker code
    pattern = r"^[A-Z]+$"
    if not re.match(pattern, ticker):
        raise argparse.ArgumentTypeError('Invalid ticker format. Expected uppercase letters only')
    return ticker

def validate_broker_string(broker):
    # Regex pattern to match IP:PORT or HOSTNAME:PORT
    pattern = r"^(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+)$"
    if not re.match(pattern, broker):
        raise argparse.ArgumentTypeError('Invalid broker string format. Expected IP:PORT or HOSTNAME:PORT')
    return broker

def validate_broker_port(port):
    try:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError()
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid broker port. Expected a valid port number (1-65535)')
    return port

def validate_topic(topic):
    if ' ' in topic:
        raise argparse.ArgumentTypeError('Invalid topic. Spaces are not allowed')
    return topic

def publish_to_kafka(ticker, kafka_topic, bootstrap_ip, bootstrap_port, mode):
    streaming_extractor = extractor.StreamingDataExtractor(ticker)
    producer = KafkaProducer(bootstrap_ip, bootstrap_port, mode)
    
    try:
        data = streaming_extractor.fetch_realtime_data()
        json_data = json.dumps(data)
        producer.send(kafka_topic, json_data)
        logging.info("Published to Kafka topic %s", kafka_topic)
    except Exception as e:
        logging.error("Failed to publish to Kafka topic %s: %s", kafka_topic, e)
        raise
    finally:
        producer.close()

def config_and_get_argparse():
    parser = argparse.ArgumentParser(description='Kafka Data Publisher')
    parser.add_argument('--ticker', help='Ticker symbol', required=True, type=validate_ticker)
    parser.add_argument('--broker_ip', help='Kafka broker server ip', required=True, type=validate_broker_string)
    parser.add_argument('--broker_port', help='Kafka broker server port', required=True, type=validate_broker_port)
    parser.add_argument('--topic', help='Kafka topic', required=True, type=validate_topic)
    parser.add_argument('--mode', help='Streaming or batch mode', required=True, choices=['streaming', 'batch'])
    args = parser.parse_args()
    
    if not all([args.ticker, args.broker_ip, args.broker_port, args.topic]):
        parser.error("Please provide all the required arguments")
    
    if not args.broker_port.isdigit():
        parser.error("Please provide a valid port number")
        
    return args