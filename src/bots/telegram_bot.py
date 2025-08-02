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

# Import the agent processing function
from src.agents.main_agent import process_query
from src.core.rate_limiter import rate_limiter
from src.core.config import config

# --- CONFIGURATION ---
# Note: logging and dotenv are configured in main.py, don't configure them again here
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- VALIDATION ---
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set.")


# --- UTILITY FUNCTIONS ---
def split_long_message(text: str, max_length: int = config.MESSAGE_MAX_LENGTH) -> list[str]:
    """
    Split a long message into chunks that fit Telegram's message length limit.
    
    Args:
        text (str): The message text to split
        max_length (int): Maximum length per message (default from config)
        
    Returns:
        list[str]: List of message chunks
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    
    # Try to split on sentences first (by periods, exclamation marks, question marks)
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Add back the period
        sentence += "."
        
        # If adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Single sentence is too long, split by words
                words = sentence.split()
                for word in words:
                    if len(current_chunk) + len(word) + 1 > max_length:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = word
                    else:
                        current_chunk += " " + word if current_chunk else word
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


# --- TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am your AI agent. How can I help you today?"
    )
    logger.info(f"User {update.effective_user.name} started a conversation.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all text messages from the user with rate limiting."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name or "Unknown"
    
    logger.info(f"Received message from {user_name} (ID: {user_id}): '{user_message}'")

    # Check rate limit
    if not rate_limiter.is_allowed(user_id):
        reset_time = rate_limiter.get_reset_time(user_id)
        minutes = int(reset_time // 60)
        seconds = int(reset_time % 60)
        
        rate_limit_msg = (
            f"⏰ You're sending messages too quickly! Please wait "
            f"{minutes}m {seconds}s before trying again."
        )
        
        await context.bot.send_message(chat_id=chat_id, text=rate_limit_msg)
        logger.warning(f"Rate limited user {user_name} (ID: {user_id})")
        return

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

        # Split long responses to respect Telegram's message length limit
        message_chunks = split_long_message(response_text)
        
        for i, chunk in enumerate(message_chunks):
            await context.bot.send_message(chat_id=chat_id, text=chunk)
            # Add small delay between chunks to avoid flooding
            if i < len(message_chunks) - 1:
                await asyncio.sleep(0.5)
        
        logger.info(f"Sent reply to {user_name} in {len(message_chunks)} part(s)")

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