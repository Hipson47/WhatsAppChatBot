# Use the official Google Python base image which includes gcloud tools.
FROM google/cloud-sdk:slim

# Set the working directory
WORKDIR /app

# Install Python and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application source code and startup script
COPY ./src ./src
COPY main.py .
COPY startup.sh .
RUN chmod +x ./startup.sh

# Create a non-root user and switch to it
RUN adduser --system --group appuser
RUN chown -R appuser:appuser /app
USER appuser

# The PORT environment variable is automatically provided by Cloud Run.
ENV PORT 8080

# The startup script will be the entrypoint
ENTRYPOINT ["./startup.sh"]