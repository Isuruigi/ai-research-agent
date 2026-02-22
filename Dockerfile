# Optimized build for Railway (< 4GB limit)
FROM python:3.11-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose port (7860 for HF Spaces, 8000 for local/other platforms)
EXPOSE 7860

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
