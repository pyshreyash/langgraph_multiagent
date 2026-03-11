from langgraph.graph import StateGraph, END, START
from langchain_core.messages import SystemMessage
from states import ScoringState
from schemas import Scores
from llm import get_llm
import json

llm = get_llm()


async def compute_score(state: ScoringState):

    data = state["discovery_data"]
    objective = state["user_objective"]

    prompt = SystemMessage(content=f"""
            You are an M&A strategy analyst.

            Score the company from 1-5 on:

            1. Financial Strength
            2. Market Sentiment
            3. Willingness to Sell

            Financial data:
            {data}

            User objective:
            {objective}

            Strictly Return JSON:
            {{
            "Financial Strength": <1-5>,
            "Market Sentiment": <1-5>,
            "Willingness to Sell": <1-5>
            }}
            """)

    response = await llm.ainvoke([prompt])

    scores = json.loads(str(response.content))

    return {"scores": scores}

scoring_graph = StateGraph(ScoringState)
scoring_graph.add_node("compute_score", compute_score)
scoring_graph.add_edge(START, "compute_score")
scoring_graph.add_edge("compute_score", END)

scoring_agent = scoring_graph.compile()