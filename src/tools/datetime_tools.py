"""
DateTime tools for the agent system.

This module provides tools for retrieving current time information
in various timezones using the pytz library.
"""

from datetime import datetime
import pytz
from langchain.tools import tool


@tool
def get_current_time(timezone: str) -> str:
    """
    Returns the current time in the specified timezone.
    
    Args:
        timezone (str): The timezone to get the current time for 
                       (e.g., 'Europe/Warsaw', 'America/New_York', 'UTC')
                       
    Returns:
        str: Formatted current time string or error message
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"The current time in {timezone} is {now.strftime('%Y-%m-%d %H:%M:%S')}."
    except pytz.UnknownTimeZoneError:
        return f"Error: Unknown timezone '{timezone}'. Please use a valid timezone like 'Europe/Warsaw' or 'UTC'."