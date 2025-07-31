"""
Telegram Bot implementation with agent-based architecture.

This module provides a Telegram bot interface that delegates user queries
to an intelligent agent system for processing and response generation.
"""

import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Import the agent processing function
from src.agents.main_agent import process_query

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- VALIDATION ---
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set.")


# --- TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am your AI agent. How can I help you today?"
    )
    logger.info(f"User {update.effective_user.name} started a conversation.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all text messages from the user."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"Received message from {update.effective_user.name}: '{user_message}'")

    try:
        # Show a "typing..." action to the user
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # Process the message using the agent executor in a non-blocking way
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(
            None,  # Use the default thread pool executor
            process_query,
            user_message
        )

        await context.bot.send_message(chat_id=chat_id, text=response_text)
        logger.info(f"Sent reply to {update.effective_user.name}: '{response_text}'")

    except Exception as e:
        error_message = f"An error occurred while processing the message: {e}"
        logger.error(error_message, exc_info=True)
        await context.bot.send_message(
            chat_id=chat_id,
            text="I'm sorry, but I encountered an error while processing your request. Please try again later."
        )


def run():
    """Runs the Telegram bot."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    logger.info("Telegram bot is running and polling for updates...")
    application.run_polling()