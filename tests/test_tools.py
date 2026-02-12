"""Test agent tools"""
import pytest
from src.tools.vector_store import VectorStore
from src.tools.scraper import WebScraper
from langchain_core.documents import Document

@pytest.mark.asyncio
async def test_vector_store_basic():
    """Test basic vector store operations"""
    vs = VectorStore(persist_directory="./test_chroma")
    
    # Create test documents
    docs = [
        Document(page_content="Python is a programming language", metadata={"source": "test"}),
        Document(page_content="LangChain is a framework for LLMs", metadata={"source": "test"})
    ]
    
    # Store
    vs.store_findings(docs, collection_name="test_collection")
    
    # Search
    results = vs.similarity_search("programming", k=1, collection_name="test_collection")
    
    assert len(results) > 0
    assert "Python" in results[0].page_content

@pytest.mark.asyncio
async def test_web_scraper():
    """Test web scraping"""
    scraper = WebScraper(chunk_size=500)
    
    # Use a reliable test URL
    chunks = await scraper.scrape_url("https://en.wikipedia.org/wiki/Python_(programming_language)")
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, Document) for chunk in chunks)
    assert all(len(chunk.page_content) <= 500 for chunk in chunks)
