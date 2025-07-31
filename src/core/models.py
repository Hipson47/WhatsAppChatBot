"""
Data models for agent commands.

This module defines Pydantic models that represent structured commands
that can be parsed from natural language input and executed by the agent system.
"""

from pydantic import BaseModel, Field
from typing import Literal, Union


class SearchKnowledgeBase(BaseModel):
    """
    Command model for searching the knowledge base.
    
    This command is used when the user asks questions that require
    information from the knowledge base documents.
    """
    task: Literal["search_knowledge_base"] = "search_knowledge_base"
    query: str = Field(..., description="The user's question to search for in the knowledge base.")


class GetCurrentTime(BaseModel):
    """
    Command model for retrieving the current time.
    
    This command is used when the user asks for the current time,
    optionally in a specific timezone.
    """
    task: Literal["get_current_time"] = "get_current_time"
    timezone: str = Field("UTC", description="The timezone to get the current time for, e.g., 'Europe/Warsaw' or 'America/New_York'. Defaults to UTC if not specified by the user.")


# A union of all possible command models
AgentCommand = Union[SearchKnowledgeBase, GetCurrentTime]