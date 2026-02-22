"""LangGraph agent orchestration"""
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import research_node, scrape_node, synthesis_node, should_continue
import logging

logger = logging.getLogger(__name__)

def create_agent():
    """Create and compile the agent graph"""
    
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("scrape", scrape_node)
    workflow.add_node("synthesize", synthesis_node)
    
    # Set entry point
    workflow.set_entry_point("research")
    
    # Add edges
    workflow.add_conditional_edges(
        "research",
        should_continue,
        {
            "scrape": "scrape",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "scrape",
        should_continue,
        {
            "synthesize": "synthesize",
            "end": END
        }
    )
    
    workflow.add_edge("synthesize", END)
    
    # Compile
    agent = workflow.compile()
    logger.info("Agent graph compiled successfully")
    
    return agent

# Global agent instance
agent = create_agent()
