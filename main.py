#!/usr/bin/env python3
"""
Main entry point for the Telegram RAG Multi-Agent Bot.

This module is responsible for starting the Telegram bot and configuring
the logging for the application. It also runs an HTTP server for Cloud Run health checks.
"""

import os
import sys
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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


def validate_environment():
    """
    Validate that all required environment variables are set.
    
    Raises:
        SystemExit: If any required environment variable is missing
    """
    required_vars = {
        "TELEGRAM_BOT_TOKEN": "Get this from @BotFather on Telegram",
        "OPENAI_API_KEY": "Get this from your OpenAI account",
        "GOOGLE_APPLICATION_CREDENTIALS": "Path to your Google Cloud service account JSON file"
    }
    
    missing_vars = []
    for var_name, description in required_vars.items():
        if not os.getenv(var_name):
            missing_vars.append(f"  {var_name}: {description}")
    
    if missing_vars:
        logging.error("Missing required environment variables:")
        for var in missing_vars:
            logging.error(var)
        logging.error("\nPlease set these variables in your .env file and restart the application.")
        logging.error("See .env.example for the template.")
        raise SystemExit(1)
    
    logging.info("✅ All required environment variables are set")


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for Cloud Run health checks."""
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default HTTP server logs to avoid spam
        pass


def run_health_server():
    """Run a simple HTTP server for health checks with error handling."""
    try:
        port = int(os.environ.get('PORT', 8080))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logging.info(f"Health check server running on 0.0.0.0:{port}")
        server.serve_forever()
    except OSError as e:
        logging.error(f"Failed to start health check server on port {port}: {e}")
        logging.error("This might be due to port already in use or permission issues")
    except KeyboardInterrupt:
        logging.info("Health check server shutdown requested")
    except Exception as e:
        logging.error(f"Unexpected error in health check server: {e}", exc_info=True)


if __name__ == "__main__":
    logging.info("Starting Telegram bot with health check server...")
    
    try:
        # Validate environment variables before starting
        validate_environment()
        
        # Start health check server in a separate thread
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        # Start the Telegram bot (main thread)
        telegram_bot.run()
        
    except KeyboardInterrupt:
        logging.info("Application shutdown requested by user")
    except SystemExit:
        # Re-raise SystemExit (from validate_environment) without logging
        raise
    except Exception as e:
        logging.error(f"Critical error in main application: {e}", exc_info=True)
        raise  # Re-raise to ensure proper exit code