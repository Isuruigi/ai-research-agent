#!/bin/bash

# Start FastAPI in the background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on the default HF port (7860)
streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0
