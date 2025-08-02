# Stage 1: Build stage with dependencies
FROM python:3.11-slim as builder
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r requirements.txt

# Stage 2: Final production stage
FROM python:3.11-slim

# Install gcloud CLI for the startup script
RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update -y && apt-get install -y google-cloud-sdk && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed packages from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application source code and startup script
COPY --chown=appuser:appuser ./src ./src
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser startup.sh .
RUN chmod +x ./startup.sh

USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Expose port
EXPOSE 8080

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# The startup script will be the entrypoint
ENTRYPOINT ["./startup.sh"]