# ingest.py
import os
import shutil
import logging
from dotenv import load_dotenv
from google.cloud import storage
from google.api_core import exceptions
from src.core.vector_store import create_vector_store, VECTOR_STORE_DIR

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PROJECT_ID = os.getenv("GCP_PROJECT_ID", os.getenv("GOOGLE_CLOUD_PROJECT"))
if not PROJECT_ID:
    raise ValueError("Google Cloud project ID is not set. Please set the GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT environment variable.")

BUCKET_NAME = f"{PROJECT_ID}-knowledge-base"

def upload_directory_to_gcs(source_directory: str, bucket_name: str):
    """Uploads the contents of a directory to a GCS bucket."""
    storage_client = storage.Client()
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' already exists.")
    except exceptions.NotFound:
        logging.info(f"Bucket '{bucket_name}' not found. Creating a new one.")
        bucket = storage_client.create_bucket(bucket_name, location="europe-west1") # Specify location
        logging.info(f"Bucket '{bucket_name}' created successfully.")

    # Clear existing vector_store objects in the bucket before uploading new ones
    blobs_to_delete = list(bucket.list_blobs(prefix=f"{VECTOR_STORE_DIR}/"))
    if blobs_to_delete:
        logging.info(f"Deleting {len(blobs_to_delete)} old objects from gs://{bucket_name}/{VECTOR_STORE_DIR}/")
        bucket.delete_blobs(blobs_to_delete)

    for root, _, files in os.walk(source_directory):
        for file in files:
            local_path = os.path.join(root, file)
            gcs_path = os.path.join(VECTOR_STORE_DIR, os.path.relpath(local_path, source_directory)).replace("\\", "/")
            
            blob = bucket.blob(gcs_path)
            logging.info(f"Uploading '{local_path}' to 'gs://{bucket_name}/{gcs_path}'")
            blob.upload_from_filename(local_path)
            
    logging.info(f"Directory '{source_directory}' uploaded successfully.")


if __name__ == "__main__":
    logging.info("--- Starting Knowledge Base Ingestion Process ---")
    
    # Step 1: Create the vector store locally
    create_vector_store()

    # Step 2: Upload the created vector store to GCS
    if os.path.exists(VECTOR_STORE_DIR):
        upload_directory_to_gcs(VECTOR_STORE_DIR, BUCKET_NAME)
    else:
        logging.error(f"Vector store directory '{VECTOR_STORE_DIR}' not found after creation process. Aborting upload.")
        # Exit with a non-zero code to fail the CI/CD step
        exit(1)
    
    logging.info("--- Knowledge Base Ingestion Process Finished Successfully ---")