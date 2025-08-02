"""
Vector Store Management for RAG Pipeline.

This module provides functionality for creating and managing ChromaDB vector stores
from documents in the knowledge base directory.
"""

import os
import shutil
import logging
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.core.config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants - using configuration
KNOWLEDGE_BASE_DIR = "knowledge_base"  # This remains hardcoded as it's the source directory


def create_vector_store():
    """
    Creates a vector store from documents in the knowledge_base directory.
    
    This function loads documents from the knowledge base, splits them into chunks,
    creates embeddings using Vertex AI, and persists them in a ChromaDB vector store.
    """
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        logging.warning(f"Knowledge base directory '{KNOWLEDGE_BASE_DIR}' not found. Skipping vector store creation.")
        return

    # Remove old vector store if it exists
    if os.path.exists(config.VECTOR_STORE_DIR):
        logging.info(f"Removing existing vector store at '{config.VECTOR_STORE_DIR}'")
        shutil.rmtree(config.VECTOR_STORE_DIR)

    # Load documents
    logging.info(f"Loading documents from '{KNOWLEDGE_BASE_DIR}'...")
    
    # Load the single consolidated knowledge base file
    loader = DirectoryLoader(
        "knowledge_base",
        glob="wiedza.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    try:
        docs = loader.load()
        if not docs:
            logging.warning("No documents found in the knowledge base.")
            return
        logging.info(f"Loaded {len(docs)} documents.")
    except Exception as e:
        logging.error(f"Failed to load documents: {e}")
        return

    # Split documents into chunks using configurable parameters
    logging.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    docs = text_splitter.split_documents(docs)
    logging.info(f"Split into {len(docs)} chunks.")

    # Initialize the embedding model with configuration
    logging.info("Initializing embedding model...")
    embeddings = VertexAIEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        **config.get_vertex_ai_config()
    )

    # Create and persist the vector store
    logging.info(f"Creating and persisting vector store at '{config.VECTOR_STORE_DIR}'...")
    try:
        db = Chroma.from_documents(docs, embeddings, persist_directory=config.VECTOR_STORE_DIR)
        logging.info("Vector store created successfully.")
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}")


if __name__ == "__main__":
    create_vector_store()