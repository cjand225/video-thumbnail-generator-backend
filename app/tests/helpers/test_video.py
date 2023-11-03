from app.helpers.video import supported_video_formats, is_supported_video_format, is_valid_resolution, is_valid_seconds, seconds_to_timestamp
import pytest

def test_supported_video_formats():
    """Test if the supported_video_formats function returns the correct list of formats."""
    formats = supported_video_formats()
    expected_formats = ["mp4", "mkv", "flv", "avi", "mov", "wmv", "webm"]
    assert formats == expected_formats, "The list of supported video formats is incorrect"

@pytest.mark.parametrize("file_name", [
    "video.mp4",
    "movie.mkv",
    "clip.flv",
    "record.avi",
    "animation.mov",
    "media.wmv",
    "stream.webm"
])
def test_is_supported_video_format_valid(file_name):
    """Test the is_supported_video_format function with valid video file names."""
    assert is_supported_video_format(file_name), f"{file_name} should be recognized as a supported video format"

@pytest.mark.parametrize("file_name", [
    "image.png",
    "document.pdf",
    "audio.mp3",
    "archive.zip",
    "script.js",
    "stylesheet.css",
    "webpage.html"
])
def test_is_supported_video_format_invalid(file_name):
    """Test the is_supported_video_format function with invalid file names."""
    assert not is_supported_video_format(file_name), f"{file_name} should not be recognized as a supported video format"

def test_is_supported_video_format_case_insensitive():
    """Test the is_supported_video_format function for case-insensitivity."""
    assert is_supported_video_format("video.MP4"), "Uppercase file extensions should be recognized as supported"
    assert not is_supported_video_format("image.PNG"), "Uppercase file extensions of unsupported types should not be recognized as supported"

def test_valid_resolutions():
    assert is_valid_resolution("1920x1080"), "1920x1080 should be a valid resolution."
    assert is_valid_resolution("1280x720"), "1280x720 should be a valid resolution."
    assert is_valid_resolution("320x240"), "320x240 should be a valid resolution."

def test_invalid_resolutions():
    assert not is_valid_resolution("1920x1200"), "1920x1200 should not be a valid resolution."
    assert not is_valid_resolution("0x0"), "0x0 should not be a valid resolution."
    assert not is_valid_resolution("abc"), "Non-numeric resolutions should not be valid."
    assert not is_valid_resolution("123x"), "Incomplete resolutions should not be valid."
    assert not is_valid_resolution("x123"), "Incomplete resolutions should not be valid."
    assert not is_valid_resolution("9999x9999"), "Resolutions too large should not be valid."
    assert not is_valid_resolution("-1920x1080"), "Negative resolutions should not be valid."

def test_valid_seconds():
    assert is_valid_seconds(0), "0 should be a valid second."
    assert is_valid_seconds(1), "1 should be a valid second."
    assert is_valid_seconds(60), "60 should be a valid second."

def test_invalid_seconds():
    assert not is_valid_seconds(-1), "-1 should not be a valid second."
    assert not is_valid_seconds(1.5), "1.5 should not be a valid second."
    assert not is_valid_seconds("a"), "'a' should not be a valid second."
    assert not is_valid_seconds(None), "None should not be a valid second."

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
