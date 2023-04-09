import sys
import platform

def test_importStreaming():
    try:
        import streaming
    except:
        assert False, "Failed to import streaming"

def test_importKafka():
    try:
        import streaming.messageQueue
    except:
        assert False, "Failed to import kafka"

def test_importUtils():
    try:
        import streaming.messageQueue.utils
    except:
        assert False, "Failed to import kafka"

def test_importUtilsUtils():
    try:
        from streaming.messageQueue.utils.util import reportLog
    except ImportError:
        assert False, "Failed to import utils"

def test_pathInsertion():
    if not "/opt/streamDAQ/srcs" in sys.path:
        assert False, "Failed to insert python path"
