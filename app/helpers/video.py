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
