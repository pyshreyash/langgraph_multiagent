from langgraph.graph import StateGraph, END
from states import ParentState, ScoringState, DiscoveryState

from agents.discovery_agent import data_discovery_agent
from agents.scoring_agent import scoring_agent


async def run_discovery(state: ParentState):
    discovery_state: DiscoveryState = {
        "company": state["company"],
        "extracted_data": {},
        "parsed_output": {},
        "messages": []
    }

    response = await data_discovery_agent.ainvoke(discovery_state)

    return {"discovery_output": response["parsed_output"]}


async def run_scoring(state: ParentState):

    scoring_state: ScoringState = {
        "company": state["company"],
        "discovery_data": state["discovery_output"],
        "scores": {},
        "user_objective": state["user_objective"]
    }

    response = await scoring_agent.ainvoke(scoring_state)

    return {"scores": response["scores"]}




graph = StateGraph(ParentState)

graph.add_node("discovery", run_discovery)
graph.add_node("scoring", run_scoring)

graph.set_entry_point("discovery")

graph.add_edge("discovery", "scoring")
graph.add_edge("scoring", END)

orchestrator = graph.compile()