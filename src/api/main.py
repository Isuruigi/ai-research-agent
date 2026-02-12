"""FastAPI application"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response Models
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=500)
    session_id: Optional[str] = None
    max_results: int = Field(default=5, ge=1, le=10)

class ResearchResponse(BaseModel):
    answer: str
    sources: list = []
    session_id: str
    timestamp: str

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

# API Key validation (optional)
API_KEY = os.getenv("API_KEY", "demo-key")

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

@app.post("/research", response_model=ResearchResponse)
async def research(
    request: ResearchRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Research endpoint - returns AI-generated research answers
    
    For demo purposes, this returns a mock response.
    In production, integrate with Groq LLM + Tavily search.
    """
    try:
        logger.info(f"Research query: {request.query}")
        
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Mock response for demo
        # TODO: Replace with actual LLM + RAG implementation
        answer = f"""Based on current research, here's what I found about your query:

**{request.query}**

This is a comprehensive topic that involves multiple aspects:

1. **Overview**: This subject has been extensively studied and continues to evolve with new discoveries and insights.

2. **Key Points**:
   - Current understanding shows significant developments in this area
   - Research indicates multiple factors contribute to this phenomenon
   - Expert consensus suggests ongoing importance of this topic

3. **Recent Developments**: The field has seen notable progress in recent years, with new methodologies and technologies enhancing our understanding.

4. **Implications**: The findings have broad implications across various sectors and continue to influence policy and practice.

*Note: This is a demo response. For full functionality with real-time research, please configure Groq API and Tavily Search API keys.*"""

        return ResearchResponse(
            answer=answer,
            sources=[],
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Research error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
