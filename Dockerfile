# Production-ready Build for Hugging Face Spaces
FROM python:3.11-slim

# Create a non-root user (Hugging Face default is 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install system dependencies (must be as root)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
USER user

# Copy requirements and install CPU-only PyTorch first
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.4.0+cpu \
    torchvision==0.19.0+cpu \
    torchaudio==2.4.0+cpu

# Install remaining dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user src/ ./src/
COPY --chown=user frontend/ ./frontend/
COPY --chown=user start.sh .

# Create persistent storage directory for ChromaDB
RUN mkdir -p chroma_db && chmod 777 chroma_db

# Ensure start.sh is executable
RUN chmod +x start.sh

# Expose port 7860 for HF Spaces
EXPOSE 7860

# Run both API and Streamlit via start.sh
CMD ["./start.sh"]
