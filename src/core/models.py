"""
Data models for agent commands.

This module defines Pydantic models that represent structured commands
that can be parsed from natural language input and executed by the agent system.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Union
import pytz


class SearchKnowledgeBase(BaseModel):
    """
    Command model for searching the knowledge base.
    
    This command is used when the user asks questions that require
    information from the knowledge base documents.
    """
    task: Literal["search_knowledge_base"] = "search_knowledge_base"
    query: str = Field(
        ..., 
        min_length=1,
        max_length=2000,
        description="The user's question to search for in the knowledge base. Must be between 1-2000 characters."
    )
    
    @validator('query')
    def validate_query(cls, v):
        """Validate that query is not just whitespace."""
        if not v.strip():
            raise ValueError("Query cannot be empty or just whitespace")
        return v.strip()


class GetCurrentTime(BaseModel):
    """
    Command model for retrieving the current time.
    
    This command is used when the user asks for the current time,
    optionally in a specific timezone.
    """
    task: Literal["get_current_time"] = "get_current_time"
    timezone: str = Field(
        "UTC", 
        description="The timezone to get the current time for, e.g., 'Europe/Warsaw' or 'America/New_York'. Defaults to UTC if not specified by the user."
    )
    
    @validator('timezone')
    def validate_timezone(cls, v):
        """Validate that timezone is a valid pytz timezone."""
        try:
            pytz.timezone(v)
            return v
        except pytz.UnknownTimeZoneError:
            # Common timezone aliases mapping
            timezone_aliases = {
                'warsaw': 'Europe/Warsaw',
                'poland': 'Europe/Warsaw', 
                'new york': 'America/New_York',
                'nyc': 'America/New_York',
                'london': 'Europe/London',
                'uk': 'Europe/London',
                'paris': 'Europe/Paris',
                'berlin': 'Europe/Berlin',
                'tokyo': 'Asia/Tokyo',
                'moscow': 'Europe/Moscow',
                'utc': 'UTC',
                'gmt': 'UTC',
            }
            
            # Try to map common names to proper timezone
            normalized = v.lower().strip()
            if normalized in timezone_aliases:
                return timezone_aliases[normalized]
            
            # If still not found, fallback to UTC
            return "UTC"


# A union of all possible command models
AgentCommand = Union[SearchKnowledgeBase, GetCurrentTime]