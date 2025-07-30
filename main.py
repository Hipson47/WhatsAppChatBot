#!/usr/bin/env python3
"""
Main entry point for the WhatsApp RAG Multi-Agent Bot.

This module is responsible for starting the uvicorn ASGI server and running
the FastAPI application with proper configuration for both development and
production environments.
"""

import os
import sys
import logging
from typing import Optional

import uvicorn
import structlog

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.main import app

# Configure basic logging for uvicorn
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = structlog.get_logger(__name__)


def get_config() -> dict:
    """
    Get server configuration from environment variables.
    
    Returns:
        dict: Configuration dictionary with server settings.
    """
    config = {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "log_level": os.getenv("LOG_LEVEL", "info").lower(),
        "reload": os.getenv("RELOAD", "false").lower() == "true",
        "workers": int(os.getenv("WORKERS", "1")),
    }
    
    # Enable reload only in development
    if os.getenv("ENVIRONMENT") == "development":
        config["reload"] = True
        config["workers"] = 1  # Reload doesn't work with multiple workers
    
    return config


def main() -> None:
    """
    Main function to start the uvicorn server.
    
    This function configures and starts the uvicorn ASGI server with the
    FastAPI application, using configuration from environment variables.
    """
    config = get_config()
    
    logger.info(
        "Starting WhatsApp RAG Multi-Agent Bot server",
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
        workers=config["workers"],
        log_level=config["log_level"]
    )
    
    try:
        # Run the server
        uvicorn.run(
            "src.api.main:app",
            host=config["host"],
            port=config["port"],
            log_level=config["log_level"],
            reload=config["reload"],
            workers=config["workers"] if not config["reload"] else 1,
            access_log=True,
            use_colors=True,
            server_header=False,
            date_header=False,
        )
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error("Failed to start server", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    main()