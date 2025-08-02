"""
Configuration settings for the AI agent system.

This module contains all configurable parameters for the application,
making it easier to maintain and modify settings without changing code.
"""

import os
from typing import Dict, Any


class Config:
    """Application configuration class with environment variable support."""
    
    # AI Model Configuration
    PARSER_MODEL: str = os.getenv("PARSER_MODEL", "gpt-4o-mini")
    EXECUTOR_MODEL: str = os.getenv("EXECUTOR_MODEL", "gpt-4o-mini") 
    SUPERVISOR_MODEL: str = os.getenv("SUPERVISOR_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "textembedding-gecko@003")
    
    # Temperature Settings
    PARSER_TEMPERATURE: float = float(os.getenv("PARSER_TEMPERATURE", "0"))
    EXECUTOR_TEMPERATURE: float = float(os.getenv("EXECUTOR_TEMPERATURE", "0.2"))
    SUPERVISOR_TEMPERATURE: float = float(os.getenv("SUPERVISOR_TEMPERATURE", "0.1"))
    
    # Vector Store Configuration  
    VECTOR_STORE_DIR: str = os.getenv("VECTOR_STORE_DIR", "vector_store")
    RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "5"))
    
    # Text Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # Telegram Configuration
    MESSAGE_MAX_LENGTH: int = int(os.getenv("MESSAGE_MAX_LENGTH", "4096"))
    
    # Rate Limiting (requests per minute per user)
    RATE_LIMIT_PER_USER: int = int(os.getenv("RATE_LIMIT_PER_USER", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
    # API Timeouts (seconds)
    OPENAI_TIMEOUT: int = int(os.getenv("OPENAI_TIMEOUT", "30"))
    VERTEX_AI_TIMEOUT: int = int(os.getenv("VERTEX_AI_TIMEOUT", "30"))
    
    # Production Settings
    VERBOSE_LOGGING: bool = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI client configuration."""
        return {
            "timeout": cls.OPENAI_TIMEOUT,
            "max_retries": 3,
        }
    
    @classmethod
    def get_vertex_ai_config(cls) -> Dict[str, Any]:
        """Get Vertex AI client configuration."""
        return {
            "timeout": cls.VERTEX_AI_TIMEOUT,
        }


# Global config instance
config = Config()