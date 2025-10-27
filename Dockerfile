# Use official Python runtime as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies with verification
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    ghostscript \
    && rm -rf /var/lib/apt/lists/* \
    && gs --version \
    && pdftoppm -v

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory with proper permissions
RUN mkdir -p /tmp/pdf_bot_temp && \
    chmod 755 /tmp/pdf_bot_temp

# Run bot as non-root user for security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app /tmp/pdf_bot_temp

USER botuser

# Verify installations on startup
RUN gs --version && echo "✅ Ghostscript verified" || echo "❌ Ghostscript missing"

# Run the bot
CMD ["python", "bot.py"]