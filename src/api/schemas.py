"""API request/response schemas"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class ResearchRequest(BaseModel):
    """Research query request"""
    query: str = Field(
        ..., 
        min_length=10, 
        max_length=500,
        description="Research question or topic"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation continuity"
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum search results to process"
    )
    
    @validator('query')
    def sanitize_query(cls, v):
        # Remove potential injection patterns
        blocked_phrases = [
            "ignore previous",
            "disregard",
            "system:",
            "assistant:",
            "<script>",
            "javascript:"
        ]
        
        v_lower = v.lower()
        for phrase in blocked_phrases:
            if phrase in v_lower:
                raise ValueError(f"Query contains blocked phrase: {phrase}")
        
        # Remove excessive whitespace
        v = re.sub(r'\s+', ' ', v).strip()
        
        return v

class ResearchResponse(BaseModel):
    """Research query response"""
    response: str = Field(..., description="Generated research report")
    sources: List[str] = Field(default_factory=list, description="Source URLs")
    session_id: str = Field(..., description="Session identifier")
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
