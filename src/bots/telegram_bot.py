"""
Telegram Bot implementation for RAG Multi-Agent system.

This module provides a Telegram bot interface using the python-telegram-bot library,
with integration points for RAG and agent logic.
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get the bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am your AI assistant. How can I help you today?"
    )
    logger.info(f"User {update.effective_user.name} started a conversation.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all text messages from the user."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"Received message from {update.effective_user.name}: '{user_message}'")

    # --- INTEGRATION POINT FOR RAG AND AGENT LOGIC ---
    # This is where we will call the function to process the query
    # and return the LLM-generated response.
    # For now, the bot will act as an echo.
    
    # Example of future integration:
    # from src.agents.main_agent import process_query
    # response_text = process_query(user_message, chat_id)
    
    response_text = f"Message received: '{user_message}'"
    
    # --- END OF INTEGRATION POINT ---

    await context.bot.send_message(chat_id=chat_id, text=response_text)
    logger.info(f"Sent reply to {update.effective_user.name}: '{response_text}'")


def run():
    """Runs the Telegram bot."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    logger.info("Telegram bot is running and polling for updates...")
    application.run_polling()