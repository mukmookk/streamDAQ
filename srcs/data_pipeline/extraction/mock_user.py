from data_pipeline.extraction.extractor import StreamingDataExtractor
from data_pipeline.extraction.extractor import HistoricalDataExtractor

TARGET_URL = 'https://finance.yahoo.com/quote/MSFT'

def streaming_extractor():

    return StreamingDataExtractor("MSFT")

def historical_extractor():

    return HistoricalDataExtractor("MSFT")

if __name__ == "__main__":
    streaming_extractor = streaming_extractor()
    historical_extractor = historical_extractor()
    print(streaming_extractor.get_response("realtime"))
    print(historical_extractor.get_response("historical"))
    
    print(streaming_extractor.fetch_realtime_data())
    print(historical_extractor.fetch_historical_data("./output.json"))
    