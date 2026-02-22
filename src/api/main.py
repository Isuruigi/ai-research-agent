"""FastAPI application"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from langchain_core.messages import HumanMessage
from .schemas import ResearchRequest, ResearchResponse, HealthResponse
from ..agent.graph import agent
from ..agent.memory import AgentMemory
from ..middleware.logging_middleware import LoggingMiddleware
import logging
import uuid
from datetime import datetime
import asyncio
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Get API key from environment
VALID_API_KEY = os.getenv("API_KEY", None)  # None = no auth required (open endpoint)

# Rate limit: default 10/minute, configurable via env
RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")

async def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key (optional - only enforced if API_KEY env var is set)"""
    if VALID_API_KEY is None:
        return None  # Open access
    if api_key == VALID_API_KEY:
        return api_key
    raise HTTPException(
        status_code=403,
        detail="Invalid or missing API Key."
    )

# Initialize FastAPI
app = FastAPI(
    title="AI Research Agent API",
    description="""
## Production-Ready AI Research Agent

Built with LangGraph + RAG for comprehensive web research.

### Features
* Multi-stage research pipeline (search → scrape → synthesize)
* Vector storage with ChromaDB for context retrieval
* Streaming responses via WebSocket
* Rate limiting and input validation
* Session-based conversation memory

### Usage
1. Send POST request to `/research` with your query
2. Or connect to WebSocket at `/ws/research` for streaming
3. Receive comprehensive research report with cited sources

### Tech Stack
* **LLM**: GPT-4 Turbo
* **Embeddings**: OpenAI text-embedding-3-small
* **Vector DB**: ChromaDB
* **Framework**: LangChain + LangGraph
* **API**: FastAPI
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Isuru Chathuranga",
        "url": "https://isuruig.com",
        "email": "your.email@example.com"
    },
    license_info={
        "name": "MIT"
    }
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Session storage
sessions = {}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from ..middleware.metrics import (
        request_count, request_duration, 
        active_connections, error_count
    )
    
    # Simple metrics response (would use prometheus_client in production)
    return {
        "requests_total": request_count._value._value if hasattr(request_count, '_value') else 0,
        "active_connections": active_connections._value._value if hasattr(active_connections, '_value') else 0,
        "errors_total": error_count._value._value if hasattr(error_count, '_value') else 0,
        "status": "ok"
    }


@app.post("/research", response_model=ResearchResponse)
@limiter.limit(RATE_LIMIT)
async def research_endpoint(
    request: Request, 
    req: ResearchRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Execute research query
    
    - **query**: Research question (10-500 chars)
    - **session_id**: Optional session ID for continuity
    - **max_results**: Max search results (1-10)
    """
    try:
        # Generate session ID if not provided
        session_id = req.session_id or str(uuid.uuid4())
        
        # Initialize or get memory
        if session_id not in sessions:
            sessions[session_id] = AgentMemory(session_id)
        
        memory = sessions[session_id]
        memory.add_message("user", req.query)
        
        # Execute agent
        state = {
            "messages": [HumanMessage(content=req.query)],
            "session_id": session_id,
            "research_findings": [],
            "scraped_content": [],
            "current_task": "research",
            "provider": req.provider,
            "error": None
        }
        
        result = await agent.ainvoke(state)
        
        # Extract response
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        response_content = result["messages"][-1].content if result.get("messages") else "No response generated"
        
        # Extract sources
        sources = []
        seen_urls = set()
        for finding in result.get('research_findings', []):
            url = finding.get('url', '')
            if url and url not in seen_urls:
                sources.append({
                    "title": finding.get('title', 'Source'),
                    "url": url
                })
                seen_urls.add(url)
        
        memory.add_message("assistant", response_content)
        
        return ResearchResponse(
            answer=response_content,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat(),
            provider=req.provider,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Research endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/research")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming research responses
    """
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    logger.info(f"WebSocket connected: {session_id}")
    
    try:
        while True:
            # Receive query
            data = await websocket.receive_json()
            query = data.get("query", "")
            
            if not query:
                await websocket.send_json({"error": "Empty query"})
                continue
            
            # Validate
            try:
                req = ResearchRequest(query=query, session_id=session_id)
            except Exception as e:
                await websocket.send_json({"error": str(e)})
                continue
            
            # Execute agent with streaming
            state = {
                "messages": [HumanMessage(content=query)],
                "session_id": session_id,
                "research_findings": [],
                "scraped_content": [],
                "current_task": "research",
                "error": None
            }
            
            await websocket.send_json({
                "type": "status",
                "message": "Starting research..."
            })
            
            # Stream agent execution
            async for chunk in agent.astream(state):
                await websocket.send_json({
                    "type": "chunk",
                    "data": chunk
                })
                await asyncio.sleep(0.1)  # Small delay for UI rendering
            
            await websocket.send_json({
                "type": "complete",
                "message": "Research complete"
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("AI Research Agent API starting up...")
    logger.info("Docs available at: /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("AI Research Agent API shutting down...")
    # Clean up sessions
    sessions.clear()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
