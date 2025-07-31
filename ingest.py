#!/usr/bin/env python3
"""
Knowledge Base Ingestion Script.

This script processes documents from the knowledge_base directory and creates
a vector store for the RAG pipeline. Run this script whenever you add or update
documents in the knowledge base.
"""

import os
import logging
from dotenv import load_dotenv

# It's crucial to load environment variables before importing other modules
# that might depend on them (e.g., for API keys).
load_dotenv()

# Now import the vector store creation function
from src.core.vector_store import create_vector_store


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    # Check if GOOGLE_APPLICATION_CREDENTIALS is set, which is required for VertexAIEmbeddings
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        logging.warning("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        logging.warning("Please set it to the path of your Google Cloud service account JSON key file.")
        # For this script, we can proceed as it might be handled by gcloud auth login, 
        # but it's a good practice to check.

    logging.info("Starting knowledge base ingestion process...")
    create_vector_store()
    logging.info("Knowledge base ingestion completed.")