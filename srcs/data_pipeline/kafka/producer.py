from data_pipeline.extraction.extractor import StreamingDataExtractor
import json
from confluent_kafka import Producer

class KafkaProducer():
    def __init__(self, bootstrap_server, bootstrap_port, mode):
        self.bootstrap_server = f'{bootstrap_server}:{bootstrap_port}'
        
        if mode == 'streaming':
            self.producer = Producer({
                'bootstrap.servers': self.bootstrap_server,
                'linger.ms': 100,
                'batch.num.messages': 1000,
                'queue.buffering.max.messages': 100000,
                'queue.buffering.max.ms': 1000,
                'queue.buffering.max.kbytes': 1000000,
                'compression.type': 'gzip'
            })
        elif mode == 'batch':
            self.producer = Producer({
                'bootstrap.servers': self.bootstrap_server,
                'linger.ms': 10000,
                'batch.num.messages': 10000,
                'queue.buffering.max.messages': 1000000,
                'queue.buffering.max.ms': 10000,
                'queue.buffering.max.kbytes': 1000000,
                'compression.type': 'gzip'
            })
        else:
            raise ValueError('Invalid mode. Expected streaming or batch')
    
    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, topic, data):
        self.producer.produce(topic, data.encode('utf-8'), callback=self.delivery_report)
        self.producer.poll(30)
        
    def produce_msg_from_file(self, file_path, topic):
        with open(file_path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for item in data:
                message = json.dumps(item)
                self.produce(topic, json.dumps(item))
            self.producer.flush()
            
    def produce_msg_from_function(self, data, topic, dumped=False):
        if not dumped:
            data = json.dumps(data)
        for item in data:
            self.produce(topic, item)
        self.producer.flush()

