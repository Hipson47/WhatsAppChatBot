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

# Copy the application code into the container
COPY ./backend/ .

# Set the port the application will run on
ENV PORT 8000
EXPOSE 8000

# The command to run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 