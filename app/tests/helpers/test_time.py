from app.helpers.time import seconds_to_timestamp
import pytest


def test_seconds_to_timestamp():
    assert seconds_to_timestamp(45) == "00:00:45", "Test failed for input: 45 seconds"
    assert seconds_to_timestamp(600) == "00:10:00", "Test failed for input: 600 seconds"
    assert seconds_to_timestamp(3665) == "01:01:05", "Test failed for input: 3665 seconds"
    assert seconds_to_timestamp(0) == "00:00:00", "Test failed for input: 0 seconds"
    assert seconds_to_timestamp(90000) == "25:00:00", "Test failed for input: 90000 seconds"

def test_negative_seconds():
    with pytest.raises(ValueError):
        seconds_to_timestamp(-5)
