"""Agent graph nodes"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from ..tools.web_search import search_web
from ..tools.scraper import WebScraper
from ..tools.vector_store import VectorStore
from .state import AgentState
import logging
import os

logger = logging.getLogger(__name__)

# Initialize tools
scraper = WebScraper()
vector_store = VectorStore()

def get_llm(provider: str):
    """Factory to get the selected LLM"""
    if provider == "openai":
        return ChatOpenAI(model="gpt-4o", temperature=0.7)
    elif provider == "anthropic":
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7)
    else:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )

async def research_node(state: AgentState) -> Dict[str, Any]:
    """Execute web search based on user query"""
    logger.info("Executing research node")
    
    try:
        query = state["messages"][-1].content
        results = await search_web(query, max_results=5)
        
        return {
            "research_findings": results,
            "current_task": "scraping"
        }
    except Exception as e:
        logger.error(f"Research node failed: {e}")
        return {"error": str(e)}

async def scrape_node(state: AgentState) -> Dict[str, Any]:
    """Scrape top search results"""
    logger.info("Executing scrape node")
    
    try:
        # Extract URLs from search results
        urls = [r.get('url') for r in state.get('research_findings', [])[:3]]
        urls = [u for u in urls if u]  # Filter None values
        
        if not urls:
            return {"current_task": "synthesis", "scraped_content": []}
        
        # Scrape and chunk content
        chunks = await scraper.scrape_multiple(urls)
        
        # Store in vector database
        if chunks:
            vector_store.store_findings(
                chunks, 
                collection_name=f"session_{state.get('session_id', 'default')}"
            )
        
        return {
            "current_task": "synthesis",
            "scraped_content": chunks
        }
        
    except Exception as e:
        logger.error(f"Scrape node failed: {e}")
        return {"error": str(e)}

async def synthesis_node(state: AgentState) -> Dict[str, Any]:
    """Generate final report using RAG"""
    logger.info(f"Executing synthesis node with provider: {state.get('provider', 'groq')}")
    
    try:
        query = state["messages"][-1].content
        session_id = state.get("session_id", "default")
        provider = state.get("provider", "groq")
        
        # Retrieve relevant context from vector store
        relevant_docs = vector_store.similarity_search(
            query=query,
            k=5,
            collection_name=f"session_{session_id}"
        )
        
        # Build context
        context = "\n\n---\n\n".join([
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        # Generate response
        prompt = f"""You are a research assistant. Based on the following research findings, provide a comprehensive, well-structured answer to the user's question.

User Question: {query}

Research Findings:
{context}

Instructions:
1. Synthesize information from multiple sources
2. Cite sources when making specific claims
3. Structure your response with clear sections
4. Highlight key insights and actionable takeaways
5. If information is contradictory, acknowledge different perspectives

Generate a detailed research report:"""

        llm = get_llm(provider)
        response = await llm.ainvoke(prompt)
        
        return {
            "messages": [AIMessage(content=response.content)],
            "current_task": "complete"
        }
        
    except Exception as e:
        logger.error(f"Synthesis node failed: {e}")
        return {"error": str(e)}

def should_continue(state: AgentState) -> str:
    """Determine next node based on current state"""
    if state.get("error"):
        return "end"
    
    task = state.get("current_task", "")
    
    if task == "scraping":
        return "scrape"
    elif task == "synthesis":
        return "synthesize"
    else:
        return "end"
