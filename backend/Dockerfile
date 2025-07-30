# --- Builder Stage ---
# This stage installs dependencies into a wheelhouse
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Install build tools
RUN pip install --no-cache-dir --upgrade pip wheel

# Copy requirements and build wheels
COPY ./backend/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Final Stage ---
# This stage is the final, lightweight production image
FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy the pre-built wheels from the builder stage and install them
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY ./backend/ .

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /usr/src/app
USER appuser

# Set the port the application will run on
ENV PORT 8000
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# The command to run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 