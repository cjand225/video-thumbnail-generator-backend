def supported_video_formats() -> list:
    """
    Returns a list of supported video file formats.

    These formats are widely popular and generally supported by various players and tools.

    Returns:
        list: A list of strings, where each string is a file extension representing a supported video format.
    """
    return ["mp4", "mkv", "flv", "avi", "mov", "wmv", "webm"]

def is_supported_video_format(filename: str) -> bool:
    """
    Checks if the given file has a supported video format based on its file extension.

    Args:
        filename (str): The name of the file including its extension.

    Returns:
        bool: True if the file's extension is in the list of supported video formats, False otherwise.
    """
    extension = filename.rsplit('.', 1)[-1].lower()
    return extension in supported_video_formats()

def supported_resolutions() -> set:
    """
    Returns a set of supported video thumbnail resolutions.

    These resolutions are widely accepted standards and provide good image quality.

    Returns:
        set: A set of strings, where each string is a resolution in the format "widthxheight".
    """
    return {
        "2560x1440",  # 1440p
        "1920x1080",  # 1080p
        "1600x900",   # HD+
        "1366x768",   # Common laptop screen
        "1280x720",   # 720p
        "1024x768",   # XGA
        "800x600",    # SVGA
        "640x480",    # VGA
        "320x240"     # QVGA
    }

def is_valid_resolution(resolution: str) -> bool: 
    """
    Validates the resolution ensuring it is within the set of supported resolutions.

    :param resolution: A string representing the resolution, e.g., "1920x1080"
    :return: True if the resolution is valid, False otherwise.
    """
    allowed_resolutions = supported_resolutions()
    return resolution in allowed_resolutions

def is_valid_seconds(seconds):
    if isinstance(seconds, int) and seconds >= 0:
        return True
    return False
