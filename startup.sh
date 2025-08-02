#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

BUCKET_NAME="${GCP_PROJECT_ID:-vortex-ai-user}-knowledge-base"
VECTOR_STORE_DIR="vector_store"

echo "🚀 Starting production container setup..."
echo "📍 Project ID: ${GCP_PROJECT_ID:-vortex-ai-user}"
echo "🪣 GCS Bucket: ${BUCKET_NAME}"

# Check if the vector store already exists. If not, download it from GCS.
if [ ! -d "$VECTOR_STORE_DIR" ]; then
  echo "📥 Vector store not found locally. Downloading from GCS bucket: gs://${BUCKET_NAME}/${VECTOR_STORE_DIR}"
  
  # Check if the bucket and vector store exist in GCS
  if gcloud storage ls "gs://${BUCKET_NAME}/${VECTOR_STORE_DIR}" >/dev/null 2>&1; then
    echo "☁️  Found vector store in GCS. Downloading..."
    
    # Use gcloud storage to recursively copy the directory
    # The '-m' flag enables multi-threaded/multi-processing copy for speed.
    gcloud storage cp -r "gs://${BUCKET_NAME}/${VECTOR_STORE_DIR}" .
    
    echo "✅ Download complete!"
    
    # Verify download
    if [ -d "$VECTOR_STORE_DIR" ]; then
      echo "✅ Vector store verified locally"
      echo "📊 Files in vector store: $(find $VECTOR_STORE_DIR -type f | wc -l)"
    else
      echo "❌ ERROR: Vector store download failed"
      exit 1
    fi
  else
    echo "❌ ERROR: Vector store not found in GCS bucket: gs://${BUCKET_NAME}/${VECTOR_STORE_DIR}"
    echo "💡 Please run the ingestion pipeline first to create the knowledge base:"
    echo "   python ingest.py"
    exit 1
  fi
else
  echo "✅ Vector store already exists locally. Skipping download."
  echo "📊 Files in vector store: $(find $VECTOR_STORE_DIR -type f | wc -l)"
fi

echo "🔧 Container setup complete!"
echo "🤖 Launching Telegram Bot application..."

# Start the main application (Telegram bot with health server)
exec python main.py