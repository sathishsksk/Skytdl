FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg for audio/video processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/
COPY .env.example .env

# Set environment variables
ENV PYTHONPATH=/app/src
ENV TMPFILE_PATH=/app/tmp

# Koyeb health check port (default 8000, override via PORT env var)
ENV PORT=8000
EXPOSE 8000

# Create temporary directory
RUN mkdir -p /app/tmp

CMD ["python", "-m", "src.main"]
