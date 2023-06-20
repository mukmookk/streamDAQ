import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from data_pipeline.extraction.extractor import StreamingDataExtractor, Extractor

TARGET_URL = "https://finance.yahoo.com/quote/AAPL"

@pytest.fixture
def streaming_extractor():
    '''
    mock StreamingDataExtractor
    '''
    mock_Extractor = Extractor('AAPL')
    return StreamingDataExtractor(mock_Extractor)


def test_get_response(streaming_extractor):
    '''
    test get_response
    '''
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.text = "Mocked Response"
        mock_get.return_value = mock_response

        response = streaming_extractor.get_response('realtime')

        # assert response.text == "Mocked Response"
        # mock_get.assert_called_once_with(TARGET_URL, timeout=60)


def test_get_response_exception(streaming_extractor, caplog):
    '''
    test get_response exception
    '''
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Test Exception")

        with pytest.raises(ValueError):
            streaming_extractor.get_response()

        assert "get_response: Test Exception" in caplog.text


def test_get_soup(streaming_extractor):
    streaming_extractor.response = Mock()
    streaming_extractor.response.text = "<html><body><p>Hello, World!</p></body></html>"

    soup = streaming_extractor.get_soup()

    assert soup.find("p").text == "Hello, World!"


def test_get_soup_exception(streaming_extractor, caplog):
    streaming_extractor.response = Mock()
    streaming_extractor.response.text = ""

    with pytest.raises(ValueError):
        streaming_extractor.get_soup()

    assert "get_soup: soup is None" in caplog.text


def test_parse_for_yahoofinance(streaming_extractor):
    raw_string = "+$100 (5%) Last Trade: 10:00 AM"
    expected_result = {
        "price": "+$100",
        "change": "+$100",
        "change_percent": "5%",
        "last_trade_time": "10:00 AM"
    }

    result = streaming_extractor.parse_for_yahoofinance(raw_string)

    assert result == expected_result


def test_fetch_realtime_data(streaming_extractor):
    '''
    test fetch_realtime_data
    '''
    streaming_extractor.last_update_time = datetime.now().strftime('%H:%M:%S')
    streaming_extractor.soup = Mock()
    streaming_extractor.soup.find.return_value = Mock()
    streaming_extractor.soup.find.return_value.text = "+$100 (5%) Last Trade: 10:00 AM"
    expected_json_data = '{"price": "+$100", "change": "+$5", \
                                "change_percent": "5%", "last_trade_time": "10:00 AM"}'
    json_data = streaming_extractor.fetch_realtime_data()

    assert json_data == expected_json_data

# Run pytest
pytest.main()
