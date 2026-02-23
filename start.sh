#!/bin/bash

# Start FastAPI in the background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait for FastAPI to be ready (up to 90 seconds)
# Uses Python since curl is not installed in the slim image
echo "Waiting for FastAPI to be ready..."
for i in $(seq 1 90); do
    if python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null; then
        echo "FastAPI is ready after ${i}s!"
        break
    fi
    echo "Still starting... (${i}/90s)"
    sleep 1
done

# Start Streamlit on the default HF port (7860)
streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0
