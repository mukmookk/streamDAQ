import main

def test_api_key():
    assert main.api_key is not None

def test_latest_price():
    response_json = main.timeSeriesDailyAdjusted()
    latest_price = main.getLatestPrice(response_json, "AAPL")
    assert latest_price is not None

def test_kafka_producer():
    response_json = main.timeSeriesDailyAdjusted()
    latest_price = main.getLatestPrice(response_json, "AAPL")
    producer = main.KafkaProducer(bootstrap_servers=['localhost:9092'],
                                  value_serializer=lambda x: dumps(x).encode('utf-8'))
    future = producer.send('nasdaq_prices', value=response_json)
    record_metadata = future.get(timeout=10)
    assert record_metadata is not None
    future = producer.send('lastest_price', value=latest_price)
    record_metadata = future.get(timeout=10)
    assert record_metadata is not None
    producer.close()