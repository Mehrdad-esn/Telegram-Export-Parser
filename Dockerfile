FROM python:3.11-slim

# Prevent Python from writing .pyc files to disk and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . ./

# Expose port used by Flask app
EXPOSE 5000

# Default command (for development). For production, use Gunicorn.
CMD ["python", "web_ui.py"]
