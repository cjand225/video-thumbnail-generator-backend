from app.helpers.video import supported_video_formats, is_supported_video_format
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
