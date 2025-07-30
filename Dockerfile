# --- Builder Stage ---
# This stage builds the Python dependencies in an optimized way
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip wheel

# Copy requirements and install dependencies to wheels directory
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Production Stage ---
# This stage creates the final, optimized production image
FROM python:3.11-slim

WORKDIR /usr/src/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels from builder stage and install them
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code
COPY src/ ./src/
COPY main.py .

# Change ownership to non-root user
RUN chown -R appuser:appuser /usr/src/app
USER appuser

# Set environment variables
ENV PYTHONPATH=/usr/src/app
ENV PORT=8000

# Expose port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]