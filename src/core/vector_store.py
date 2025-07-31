"""
Vector Store Management for RAG Pipeline.

This module provides functionality for creating and managing ChromaDB vector stores
from documents in the knowledge base directory.
"""

import os
import shutil
import logging
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
KNOWLEDGE_BASE_DIR = "knowledge_base"
VECTOR_STORE_DIR = "vector_store"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


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
    if os.path.exists(VECTOR_STORE_DIR):
        logging.info(f"Removing existing vector store at '{VECTOR_STORE_DIR}'")
        shutil.rmtree(VECTOR_STORE_DIR)

    # Load documents
    logging.info(f"Loading documents from '{KNOWLEDGE_BASE_DIR}'...")
    
    # Using a generic DirectoryLoader with specific loaders for each file type
    # This is more robust than a single loader for mixed content.
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="**/*",
        loader_map={
            ".md": UnstructuredMarkdownLoader,
            ".txt": TextLoader,
        },
        show_progress=True,
        use_multithreading=True
    )

    try:
        documents = loader.load()
        if not documents:
            logging.warning("No documents found in the knowledge base.")
            return
        logging.info(f"Loaded {len(documents)} documents.")
    except Exception as e:
        logging.error(f"Failed to load documents: {e}")
        return

    # Split documents into chunks
    logging.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(docs)} chunks.")

    # Initialize the embedding model
    logging.info("Initializing embedding model...")
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003")

    # Create and persist the vector store
    logging.info(f"Creating and persisting vector store at '{VECTOR_STORE_DIR}'...")
    try:
        db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_STORE_DIR)
        logging.info("Vector store created successfully.")
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}")


if __name__ == "__main__":
    create_vector_store()