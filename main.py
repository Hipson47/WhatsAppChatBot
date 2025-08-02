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
    """Run a simple HTTP server for health checks."""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logging.info(f"Health check server running on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    logging.info("Starting Telegram bot with health check server...")
    
    # Start health check server in a separate thread
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Start the Telegram bot (main thread)
    telegram_bot.run()