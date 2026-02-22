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
COPY frontend/ ./frontend/
COPY start.sh .

# Ensure start.sh is executable
RUN chmod +x start.sh

# Expose port 7860 for HF Spaces
EXPOSE 7860

# Run both API and Streamlit via start.sh
CMD ["./start.sh"]
