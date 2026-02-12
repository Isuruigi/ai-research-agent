"""FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Research Agent API",
    description="Production-Ready AI Research Agent built with LangGraph + RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("AI Research Agent API starting up...")
    logger.info("Docs available at: /docs")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ai-research-agent"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Research Agent API",
        "docs": "/docs",
        "health": "/health"
    }
