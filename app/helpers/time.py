def seconds_to_timestamp(seconds: int) -> str:
    """
    Converts a duration from seconds to a timestamp format.

    This function takes an integer representing a duration in seconds, 
    and converts it to a formatted timestamp string in the format of "HH:MM:SS".

    Args:
        seconds (int): The duration in seconds. Must be non-negative.

    Returns:
        str: A string representing the formatted timestamp.

    Raises:
        ValueError: If the input seconds is negative.

    Examples:
        >>> seconds_to_timestamp(3665)
        '01:01:05'
        
        >>> seconds_to_timestamp(3600)
        '01:00:00'
        
        >>> seconds_to_timestamp(63)
        '00:01:03'
        
        >>> seconds_to_timestamp(0)
        '00:00:00'
    """
    if seconds < 0:
        raise ValueError("Input seconds must be non-negative")

    # Calculate the number of hours and the remainder
    hours, remainder = divmod(seconds, 3600)
    
    # Calculate the number of minutes and the remaining seconds
    minutes, seconds = divmod(remainder, 60)
    
    # Format and return the timestamp string
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
