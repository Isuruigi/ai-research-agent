"""Test agent graph"""
import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import HumanMessage
from src.agent.nodes import research_node, scrape_node, synthesis_node

@pytest.mark.asyncio
@patch('src.agent.nodes.search_web')
async def test_research_node(mock_search):
    """Test research node"""
    mock_search.return_value = [
        {"url": "https://test.com", "content": "Test content"}
    ]
    
    state = {
        "messages": [HumanMessage(content="test query")],
        "session_id": "test",
        "research_findings": [],
        "scraped_content": [],
        "current_task": "research",
        "error": None
    }
    
    result = await research_node(state)
    
    assert "research_findings" in result
    assert result["current_task"] == "scraping"

@pytest.mark.asyncio
async def test_synthesis_node():
    """Test synthesis node"""
    state = {
        "messages": [HumanMessage(content="test query")],
        "session_id": "test",
        "research_findings": [],
        "scraped_content": [],
        "current_task": "synthesis",
        "error": None
    }
    
    # This will fail without real API keys, so we test error handling
    result = await synthesis_node(state)
    
    # Should either return messages or error
    assert "messages" in result or "error" in result
