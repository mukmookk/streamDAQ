from kafka import KafkaProducer
from time import sleep
import json

producer = KafkaProducer(bootstrap_servers=[bootstrap_servers], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

num_messages = 10000
message_payload = {"message": "This is a test message."}

for i in range(num_messages):
    producer.send('test_topic', value=message_payload)
    sleep(0.001)

producer.close()