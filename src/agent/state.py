"""Agent state definition"""
from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """State passed between nodes in the agent graph"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_findings: List[Dict]
    scraped_content: List
    current_task: str
    session_id: str
    provider: str
    error: str | None
