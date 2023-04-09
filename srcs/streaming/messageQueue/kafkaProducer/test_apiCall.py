import sys
import platform

def test_importStreaming():
    try:
        import streaming
    except:
        assert False, "Failed to import streaming"

def test_importKafka():
    try:
        import streaming.kafka
    except:
        assert False, "Failed to import kafka"

def test_importUtils():
    try:
        import streaming.kafka.utils
    except:
        assert False, "Failed to import kafka"

def test_importUtilsUtils():
    try:
        from streaming.kafka.utils.utils import reportLog
    except ImportError:
        assert False, "Failed to import utils"

def test_pathInsertion():
    if not "/opt/streamDAQ/srcs" in sys.path:
        print(sys.path)
        assert False, "Failed to insert python path"