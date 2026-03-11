from typing import TypedDict, Dict, Any, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class DiscoverFinancials(TypedDict):
    company: str
    financials_search: Annotated[Sequence[BaseMessage], add_messages]

class DiscoverNews(TypedDict):
    company: str
    news_search: Annotated[Sequence[BaseMessage], add_messages]

class DiscoverRumors(TypedDict):
    company: str
    rumors_search: Annotated[Sequence[BaseMessage], add_messages]

class DiscoveryState(TypedDict):
    company: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    extracted_data: Dict[str, Any]
    parsed_output: Dict[str, Any]

class ScoringState(TypedDict):
    company: str
    discovery_data: Dict[str, Any]
    user_objective: str
    scores: Dict[str, Any]

class ParentState(TypedDict):
    company: str
    discovery_output: Dict[str, Any]
    scoring_output: Dict[str, Any]
    user_objective: str
    scores: Dict[str, Any]