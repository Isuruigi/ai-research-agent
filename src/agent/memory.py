"""Conversation memory management"""
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

class AgentMemory:
    def __init__(self, session_id: str, redis_url: str = None):
        self.session_id = session_id
        redis_url = redis_url or os.getenv("REDIS_URL")
        
        # Only try Redis if URL is provided
        if redis_url:
            try:
                self.history = RedisChatMessageHistory(
                    session_id=session_id,
                    url=redis_url,
                    ttl=3600  # 1 hour TTL
                )
                logger.info(f"Memory initialized with Redis for session: {session_id}")
            except Exception as e:
                logger.warning(f"Redis unavailable, using in-memory storage: {e}")
                self.history = InMemoryChatMessageHistory()
        else:
            logger.info(f"Using in-memory storage for session: {session_id}")
            self.history = InMemoryChatMessageHistory()
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        if role == "user":
            self.history.add_user_message(content)
        elif role == "assistant":
            self.history.add_ai_message(content)
    
    def get_history(self) -> list:
        """Retrieve conversation history"""
        return self.history.messages
    
    def clear(self):
        """Clear conversation history"""
        self.history.clear()
        logger.info(f"Memory cleared for session: {self.session_id}")

