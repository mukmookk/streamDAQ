import pytest
import logging
from . import config

def test_reportlog(caplog):
    msg = 'Test log message'
    level = 'info'

    config.reportlog(msg, level)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == msg
    assert caplog.records[0].levelname == level.upper()

    caplog.clear()

    level = 'invalid-level'

    config.reportlog(msg, level)

    assert len(caplog.records) == 2
    assert caplog.records[0].message == msg
    assert caplog.records[0].levelname == level.upper()
    assert caplog.records[1].levelname == 'FATAL'