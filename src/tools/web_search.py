"""Web search tool using Tavily API"""
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def create_search_tool(max_results: int = 5):
    """Create Tavily search tool with advanced search depth"""
    return TavilySearchResults(
        max_results=max_results,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_domains=[],
        exclude_domains=["facebook.com", "twitter.com"]
    )

async def search_web(query: str, max_results: int = 10) -> List[Dict]:
    """
    Execute web search and return structured results
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with url, title, content, score
    """
    try:
        search_tool = create_search_tool(max_results)
        results = search_tool.invoke({"query": query})
        logger.info(f"Search completed: {len(results)} results for '{query}'")
        return results
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
