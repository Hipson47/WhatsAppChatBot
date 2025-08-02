# Stage 1: Build stage with dependencies
FROM python:3.11-slim as builder
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r requirements.txt

# Stage 2: Final production stage
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies from wheels
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application source code and startup script
COPY --chown=appuser:appuser ./src ./src
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser startup.sh .
RUN chmod +x ./startup.sh

USER appuser

# The PORT environment variable is automatically provided by Cloud Run.
ENV PORT 8080

# The startup script will be the main command
CMD ["./startup.sh"]