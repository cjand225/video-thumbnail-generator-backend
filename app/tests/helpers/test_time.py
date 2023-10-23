from app.helpers.time import seconds_to_timestamp
import pytest

def test_seconds_to_timestamp():
    """
    Test the conversion of various durations in seconds to a timestamp format.
    
    This test checks the correct conversion of the seconds to a "HH:MM:SS" format. 
    It tests various scenarios including the lower edge case (0 seconds) and a 
    large number of seconds.
    """
    
    # Test for 45 seconds
    assert seconds_to_timestamp(45) == "00:00:45", "Test failed for input: 45 seconds"
    
    # Test for 10 minutes (600 seconds)
    assert seconds_to_timestamp(600) == "00:10:00", "Test failed for input: 600 seconds"
    
    # Test for 1 hour, 1 minute, and 5 seconds (3665 seconds)
    assert seconds_to_timestamp(3665) == "01:01:05", "Test failed for input: 3665 seconds"
    
    # Test for 0 seconds
    assert seconds_to_timestamp(0) == "00:00:00", "Test failed for input: 0 seconds"
    
    # Test for 25 hours (90000 seconds)
    assert seconds_to_timestamp(90000) == "25:00:00", "Test failed for input: 90000 seconds"

def test_negative_seconds():
    """
    Test that the function raises a ValueError when provided with a negative value for seconds.
    
    The function should raise a ValueError when negative seconds are provided 
    as it's not a valid duration for the timestamp format.
    """
    
    with pytest.raises(ValueError):
        seconds_to_timestamp(-5)
