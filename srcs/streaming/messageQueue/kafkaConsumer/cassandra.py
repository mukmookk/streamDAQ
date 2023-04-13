from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from kafka import KafkaConsumer
import os
import json
import config

bootstrap_servers = os.environ.get('BOOTSTRAP_SERVERS')
consumer_group_id = 'cassandra_consumer'
api_key = os.environ.get('APIKEY')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
keyspace = os.environ.get('KEYSPACE')

def connect_to_cassandra():
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([bootstrap_servers], auth_provider=auth_provider)
    session = cluster.connect(keyspace)
    return session

def insert_to_cassandra(session, data):
    symbol = data['Meta Data']['2. Symbol']
    last_refreshed = data['Meta Data']['3. Last Refreshed']
    time_series = data['Time Series (15min)']
    for time, values in time_series.items():
        open_price = float(values['1. open'])
        high_price = float(values['2. high'])
        low_price = float(values['3. low'])
        close_price = float(values['4. close'])
        volume = int(values['5. volume'])
        query = f"INSERT INTO prices (symbol, last_refreshed, time, open_price, high_price, low_price, close_price, volume) " \
                f"VALUES ('{symbol}', '{last_refreshed}', '{time}', {open_price}, {high_price}, {low_price}, {close_price}, {volume})"
        session.execute(query)

def main():
    if api_key is None:
        config.reportlog("Environment variable 'APIKEY' not found", "error")
        raise ValueError("Environment variable 'APIKEY' not found")
    else:
        config.reportlog("API Key Successfully connected", 'info')

    # Connect to Kafka Consumer
    consumer = KafkaConsumer(
        
        
        _name,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=consumer_group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Connect to Cassandra
    session = connect_to_cassandra()
    
    # Start consuming messages from Kafka topic
    for message in consumer:
        response_json = message.value
        try:
            insert_to_cassandra(session, response_json)
            config.reportlog(f"Symbol: {symbol} successfully inserted into Cassandra", 'info')
        except Exception as e:
            error_msg = f"Error inserting data into Cassandra: {e}"
            config.reportlog(error_msg, 'error')

if __name__ == '__main__':
    main()
