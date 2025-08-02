#!/usr/bin/env python3
"""
Production-Grade Knowledge Base Ingestion Script with GCS Integration.

This script processes documents from the knowledge_base directory, creates
a vector store locally, and then uploads it to Google Cloud Storage for
persistent, scalable storage. This enables automated RAG pipeline deployment.
"""

import os
import logging
import shutil
from dotenv import load_dotenv
from google.cloud import storage
from src.core.vector_store import create_vector_store

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

VECTOR_STORE_DIR = "vector_store"
BUCKET_NAME = f"{os.getenv('GCP_PROJECT_ID', 'vortex-ai-user')}-knowledge-base"


def upload_directory_to_gcs(source_directory, bucket_name):
    """Uploads the contents of a directory to a GCS bucket."""
    storage_client = storage.Client()
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
        logging.info(f"Using existing bucket: {bucket_name}")
    except Exception:
        logging.info(f"Bucket {bucket_name} not found. Creating a new one.")
        bucket = storage_client.create_bucket(bucket_name)
        logging.info(f"Bucket {bucket_name} created successfully.")

    files_uploaded = 0
    for root, _, files in os.walk(source_directory):
        for file in files:
            local_path = os.path.join(root, file)
            # Create a relative path for the blob name
            relative_path = os.path.relpath(local_path, source_directory)
            blob = bucket.blob(os.path.join(VECTOR_STORE_DIR, relative_path))
            
            logging.info(f"Uploading {local_path} to gs://{bucket_name}/{blob.name}")
            blob.upload_from_filename(local_path)
            files_uploaded += 1
    
    logging.info(f"Successfully uploaded {files_uploaded} files from {source_directory} to gs://{bucket_name}/{VECTOR_STORE_DIR}")


if __name__ == "__main__":
    logging.info("🚀 Starting production-grade knowledge base ingestion process...")
    
    # Step 1: Create the vector store locally
    logging.info("📚 Step 1: Creating vector store locally...")
    create_vector_store()
    
    # Step 2: Upload the created vector store to GCS
    logging.info("☁️  Step 2: Uploading vector store to Google Cloud Storage...")
    if os.path.exists(VECTOR_STORE_DIR):
        upload_directory_to_gcs(VECTOR_STORE_DIR, BUCKET_NAME)
        logging.info("✅ Knowledge base ingestion and GCS upload completed successfully!")
        logging.info(f"📍 Vector store is now available at: gs://{BUCKET_NAME}/{VECTOR_STORE_DIR}")
    else:
        logging.error("❌ Vector store directory not found after creation process. Cannot upload to GCS.")
        exit(1)