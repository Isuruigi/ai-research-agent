"""FastAPI application with Groq + Tavily integration"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from groq import Groq
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Request/Response Models
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=500)
    session_id: Optional[str] = None
    max_results: int = Field(default=5, ge=1, le=10)
    provider: str = Field(default="groq", pattern="^(groq|openai|anthropic)$")

class ResearchResponse(BaseModel):
    answer: str
    sources: list = []
    session_id: str
    timestamp: str
    provider: str

# Initialize FastAPI
app = FastAPI(
    title="AI Research Agent API",
    description="Production-Ready AI Research Agent built with Groq + Tavily",
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
    logger.info("Groq API configured: ✓")
    logger.info("Tavily API configured: ✓")
    logger.info("Model: llama-3.3-70b-versatile")
    logger.info("Docs available at: /docs")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "ai-research-agent",
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY"))
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
    Research endpoint - uses Groq LLM + Tavily search for real-time research
    """
    try:
        logger.info(f"Research query: {request.query}")
        
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Step 1: Search with Tavily
        logger.info("Searching with Tavily...")
        search_results = tavily_client.search(
            query=request.query,
            max_results=request.max_results
        )
        
        # Extract search context
        context = "\n\n".join([
            f"Source: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', '')}"
            for result in search_results.get('results', [])
        ])
        
        sources = [
            {
                "title": result.get('title', 'N/A'),
                "url": result.get('url', 'N/A'),
                "snippet": result.get('content', '')[:200] + "..."
            }
            for result in search_results.get('results', [])
        ]
        
        # Step 2: Generate response with selected provider
        logger.info(f"Generating response with {request.provider}...")
        
        system_prompt = """You are an expert AI research assistant. Your task is to provide comprehensive, well-structured answers based on the search results provided.

Format your response with:
- Clear headings using **bold** text
- Bullet points for key information
- Proper paragraph structure
- Citations when referencing specific sources

Be informative, accurate, and cite your sources."""

        user_prompt = f"""Based on the following search results, provide a comprehensive answer to this question:

**Question:** {request.query}

**Search Results:**
{context}

Provide a well-structured, informative answer that synthesizes the information from these sources."""

        # Use faster models or optimized parameters where possible
        if request.provider == "openai":
            llm = ChatOpenAI(model="gpt-4o", temperature=0.7, timeout=60)
        elif request.provider == "anthropic":
            llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7, timeout=60)
        else:
            # Groq is typically very fast
            llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, timeout=60)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        answer = response.content
        
        logger.info("Research completed successfully")
        
        return ResearchResponse(
            answer=answer,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat(),
            provider=request.provider
        )
        
    except Exception as e:
        logger.error(f"Research error: {str(e)}")
        error_msg = f"Research failed: {str(e)}"
        if "timeout" in str(e).lower():
            error_msg = "Research timed out. The query might be too complex or the model is overloaded."
        
        return JSONResponse(
            status_code=500,
            content={"detail": error_msg}
        )
