#!/bin/sh
set -e

# Use GCP_PROJECT_ID if set, otherwise fall back to GOOGLE_CLOUD_PROJECT
PROJECT_ID=${GCP_PROJECT_ID:-$GOOGLE_CLOUD_PROJECT}
BUCKET_NAME="${PROJECT_ID}-knowledge-base"
VECTOR_STORE_DIR="vector_store"

echo "Container starting..."
echo "Project ID: $PROJECT_ID"
echo "Bucket Name: $BUCKET_NAME"

if [ -z "$PROJECT_ID" ]; then
  echo "Error: GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT env var not set."
  exit 1
fi

if [ ! -d "$VECTOR_STORE_DIR" ]; then
  echo "Vector store not found locally. Downloading from GCS..."
  
  # Using gsutil which is part of the base gcloud-sdk image is more reliable
  gsutil -m cp -r "gs://${BUCKET_NAME}/${VECTOR_STORE_DIR}" .
  
  echo "Download complete."
else
  echo "Vector store already present. Skipping download."
fi

echo "Launching application on port ${PORT}..."
exec uvicorn src.api.webhook_handler:app --host 0.0.0.0 --port ${PORT:-8080}