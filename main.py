#!/usr/bin/env python3
"""
Main entry point for the Telegram RAG Multi-Agent Bot.

This module is responsible for starting the Telegram bot and configuring
the logging for the application.
"""

import os
import sys
import logging

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.bots import telegram_bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    logging.info("Starting Telegram bot...")
    telegram_bot.run()