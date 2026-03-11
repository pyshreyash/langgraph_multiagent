
from langgraph.graph import StateGraph, END, START
import asyncio
from states import DiscoveryState, DiscoverFinancials, DiscoverNews, DiscoverRumors
from llm import get_llm
from schemas import DiscoveryOutput
from utils import validate_with_retry
from tools import tavily_search
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from discovery_search_nodes import financials_graph, news_graph, rumors_graph
from prompts import financials_search_prompt, news_search_prompt, rumors_search_prompt
from langchain_core.messages import ToolMessage
import json

llm = get_llm()
    
async def collect_data(state: DiscoveryState) -> DiscoveryState:
    company = state['company']
    
    financials_state: DiscoverFinancials = {"company": company,
                                            "financials_search": [financials_search_prompt(company)]}

    news_state: DiscoverNews = {"company": company,
                                "news_search": [news_search_prompt(company)]}

    rumors_state: DiscoverRumors = {"company": company,
                                    "rumors_search": [rumors_search_prompt(company)]}

    financials_output, news_output, rumors_output = await asyncio.gather(financials_graph.ainvoke(financials_state), news_graph.ainvoke(news_state), rumors_graph.ainvoke(rumors_state))

    def extract_tool_messages(messages):
        return [m.content for m in messages if isinstance(m, ToolMessage)]

    return {"extracted_data" : {
        "financials": extract_tool_messages(financials_output["financials_search"]),
        "news": extract_tool_messages(news_output["news_search"]),
        "rumors": extract_tool_messages(rumors_output["rumors_search"])
    }} # type: ignore



async def parse_output(state: DiscoveryState) -> DiscoveryState:

    data = state["extracted_data"]

    prompt = SystemMessage(content=f"""
                You are an M&A research analyst.

                Analyze the following research outputs and extract structured information.

                Return STRICT JSON with this schema:

                {{
                "Revenue": "<number with currency if available>",
                "EBITDA Margin": "<percentage if available>",
                "Market Sentiment News": "<50-100 word summary>",
                "Selling Rumors": "<50-100 word summary>"
                }}

                Rules:
                - Use only the provided information.
                - If revenue or EBITDA margin cannot be determined, return "Unknown".
                - News summary must reflect overall market sentiment.
                - Rumor summary must describe acquisition or selling speculation.

                Financials data:
                {data["financials"]}

                News data:
                {data["news"]}

                Rumors data:
                {data["rumors"]}
                """)

    response = await llm.ainvoke([prompt, *state["messages"]])
    raw = str(response.content)
    # assume model outputs JSON text
    try:
        parsed_json = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Parser Error: invalid JSON\n{raw}") from e


    return {"parsed_output": parsed_json} # type: ignore

data_discovery_graph = StateGraph(DiscoveryState)
data_discovery_graph.add_node("collect_data", collect_data)
data_discovery_graph.add_node("parse_output", parse_output)
data_discovery_graph.add_edge(START, "collect_data")
data_discovery_graph.add_edge("collect_data", "parse_output")
data_discovery_graph.add_edge("parse_output", END)

data_discovery_agent = data_discovery_graph.compile()