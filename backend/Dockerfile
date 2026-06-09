# Multi-stage build for smaller runtime image
# Builder: install dependencies into a virtualenv
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install build deps required by some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment where dependencies will be installed
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Final image: copy venv and application code
FROM python:3.11-slim

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Create a non-root user
RUN adduser --disabled-password --gecos "" app \
    && mkdir -p /app

WORKDIR /app

# Copy only the venv from the builder stage (keeps /app mountable for dev)
COPY --from=builder /opt/venv /opt/venv

# Copy application code; in development this path will be mounted from the host
COPY --chown=app:app . /app

ENV PYTHONPATH=/app

# Use a non-root user for security
USER app

EXPOSE 8000

# Default command (development override via docker-compose to enable --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
