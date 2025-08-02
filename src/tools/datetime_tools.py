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
    Returns the current time in the specified timezone with detailed information.
    
    Args:
        timezone (str): The timezone to get the current time for 
                       (e.g., 'Europe/Warsaw', 'America/New_York', 'UTC')
                       
    Returns:
        str: Formatted current time string with timezone info or error message
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        # Get timezone name and offset
        tz_name = now.strftime('%Z')
        offset = now.strftime('%z')
        
        # Format offset nicely (e.g., +0100 -> +01:00)
        if len(offset) == 5:
            offset = f"{offset[:3]}:{offset[3:]}"
        
        # Get day of week
        day_name = now.strftime('%A')
        
        # Check if DST is active
        dst_info = ""
        if hasattr(tz, 'dst') and tz.dst(now):
            dst_info = " (DST active)"
        
        # Format comprehensive response
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        return (
            f"🕐 Current time in {timezone}:\n"
            f"📅 {day_name}, {time_str}\n"
            f"🌍 Timezone: {tz_name} (UTC{offset}){dst_info}"
        )
        
    except pytz.UnknownTimeZoneError:
        # Provide helpful suggestions
        common_timezones = [
            'UTC', 'Europe/Warsaw', 'Europe/London', 'Europe/Paris',
            'America/New_York', 'America/Los_Angeles', 'Asia/Tokyo'
        ]
        
        return (
            f"❌ Unknown timezone: '{timezone}'\n\n"
            f"💡 Try one of these common timezones:\n" +
            "\n".join(f"  • {tz}" for tz in common_timezones) +
            f"\n\nOr visit: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        )
        
    except Exception as e:
        return f"❌ Error getting time: {str(e)}"