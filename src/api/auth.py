"""API Key authentication for production"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import secrets
import logging

logger = logging.getLogger(__name__)

# API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify API key from request header.
    
    Usage in endpoints:
        @app.get("/protected", dependencies=[Depends(verify_api_key)])
        async def protected_endpoint():
            return {"message": "Access granted"}
    
    Client usage:
        headers = {"X-API-Key": "your-api-key"}
        response = requests.get(url, headers=headers)
    """
    # Get valid API keys from environment (comma-separated)
    valid_keys = os.getenv("API_KEYS", "").split(",")
    
    # If no API keys configured, allow all (development mode)
    if not valid_keys or valid_keys == [""]:
        logger.warning("API_KEYS not configured - auth disabled!")
        return "dev-mode"
    
    # Check if provided key is valid
    if not api_key or not secrets.compare_digest(api_key, valid_keys[0]):
        logger.warning(f"Invalid API key attempt: {api_key[:8]}..." if api_key else "No key provided")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    
    logger.info("API key verified successfully")
    return api_key


def generate_api_key() -> str:
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)


if __name__ == "__main__":
    # Generate a new API key for production
    print("Generated API Key:")
    print(generate_api_key())
    print("\nAdd to .env:")
    print(f"API_KEYS={generate_api_key()}")
