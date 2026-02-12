"""Request logging and observability"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Extract request info
        request_id = request.headers.get("X-Request-ID", str(time.time()))
        
        # Log request
        logger.info(json.dumps({
            "event": "request_started",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(json.dumps({
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "timestamp": datetime.utcnow().isoformat()
            }))
            
            # Add response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(duration)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(json.dumps({
                "event": "request_failed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "duration_ms": round(duration * 1000, 2),
                "timestamp": datetime.utcnow().isoformat()
            }))
            
            raise
