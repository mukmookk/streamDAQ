from data_pipeline.extraction.extractor import StreamingDataExtractor
import json
from confluent_kafka import Producer

class KafkaProducer():
    def __init__(self, hostname, port):
        self.hostnaem = hostname
        self.port = port
        self.producer = Producer({'bootstrap.servers': f'{self.hostnaem}:{self.port}'})

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, topic, data):
        self.producer.produce(topic, data.encode('utf-8'), callback=self.delivery_report)
        self.producer.poll(0)
        
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
        
    def flush(self):
        self.producer.flush()

if __name__ == "__main__":
    pass