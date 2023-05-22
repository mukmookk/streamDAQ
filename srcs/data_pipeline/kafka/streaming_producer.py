from data_pipeline.extraction.extractor import StreamingDataExtractor
import json
from confluent_kafka import Producer

class KafkaProducer():
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': 'kafka1:9092'})

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, topic, data):
        self.producer.produce(topic, data.encode('utf-8'), callback=self.delivery_report)
        self.producer.poll(0)

    def flush(self):
        self.producer.flush()

