"""
Data models for agent commands.

This module defines Pydantic models that represent structured commands
that can be parsed from natural language input and executed by the agent system.
"""

from pydantic import BaseModel, Field
from typing import Literal


class SearchKnowledgeBase(BaseModel):
    """
    Command model for searching the knowledge base.
    
    This command is used when the user asks questions that require
    information from the knowledge base documents.
    """
    task: Literal["search_knowledge_base"] = "search_knowledge_base"
    query: str = Field(..., description="The user's question to search for in the knowledge base.")