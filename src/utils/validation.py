"""Input validation and sanitization"""
import re
from typing import Optional
from fastapi import HTTPException

class InputValidator:
    # Blocked patterns
    INJECTION_PATTERNS = [
        r'ignore\s+previous',
        r'disregard',
        r'system\s*:',
        r'assistant\s*:',
        r'<\s*script',
        r'javascript\s*:',
        r'eval\s*\(',
        r'exec\s*\(',
        r'__import__'
    ]
    
    @staticmethod
    def sanitize_query(query: str, max_length: int = 500) -> str:
        """
        Sanitize user input
        
        Raises:
            HTTPException: If validation fails
        """
        # Check length
        if len(query) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Query too long (max {max_length} chars)"
            )
        
        if len(query.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Query too short (min 10 chars)"
            )
        
        # Check for injection patterns
        query_lower = query.lower()
        for pattern in InputValidator.INJECTION_PATTERNS:
            if re.search(pattern, query_lower):
                raise HTTPException(
                    status_code=400,
                    detail="Query contains blocked pattern"
                )
        
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Remove control characters
        query = ''.join(char for char in query if char.isprintable() or char.isspace())
        
        return query
    
    @staticmethod
    def validate_session_id(session_id: Optional[str]) -> str:
        """Validate session ID format"""
        if not session_id:
            import uuid
            return str(uuid.uuid4())
        
        # Must be UUID format
        if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', session_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid session ID format"
            )
        
        return session_id
