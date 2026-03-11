from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langgraph.graph.state import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from states import DiscoverFinancials, DiscoverNews, DiscoverRumors
from tools import tavily_search
from llm import get_llm
from tools import tavily_search


myllm = get_llm()

async def financials_search(state: DiscoverFinancials) -> DiscoverFinancials:
    response = await myllm.ainvoke(state["financials_search"])

    return {"financials_search": [response], "company": state['company']}


async def news_search(state: DiscoverNews) -> DiscoverNews:
    response = await myllm.ainvoke(state["news_search"])

    return {"news_search": [response], "company": state['company']}


async def rumors_search(state: DiscoverRumors) -> DiscoverRumors:
    response = await myllm.ainvoke(state["rumors_search"])

    return {"rumors_search": [response], "company": state['company']}

def make_should_continue(buffer_key: str):
    def should_continue(state):
        messages = state[buffer_key]
        last_message = messages[-1]
        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"
    
    return should_continue

should_continue_financials = make_should_continue("financials_search")
should_continue_news = make_should_continue("news_search")
should_continue_rumors = make_should_continue("rumors_search")

tool_node = ToolNode(tools=[tavily_search])

financials_search_graph = StateGraph(DiscoverFinancials)
financials_search_graph.add_node("tools", tool_node)
financials_search_graph.add_node("financials_search", financials_search)
financials_search_graph.add_edge(START, "financials_search")

financials_search_graph.add_conditional_edges(
    "financials_search",
    should_continue_financials,
    {
        "continue": "tools",
        "end": END
    }
)
financials_search_graph.add_edge("tools", "financials_search")
financials_graph = financials_search_graph.compile()


# News Search Sub Graph
news_search_graph = StateGraph(DiscoverNews)
news_search_graph.add_node("tools", tool_node)
news_search_graph.add_node("news_search", news_search)
news_search_graph.add_edge(START, "news_search")

news_search_graph.add_conditional_edges(
    "news_search",
    should_continue_news,
    {
        "continue": "tools",
        "end": END
    }
)
news_search_graph.add_edge("tools", "news_search")
news_graph = news_search_graph.compile()

# Rumors Sub Graph
rumors_search_graph = StateGraph(DiscoverRumors)
rumors_search_graph.add_node("tools", tool_node)
rumors_search_graph.add_node("rumors_search", rumors_search)
rumors_search_graph.add_edge(START, "rumors_search")

rumors_search_graph.add_conditional_edges(
    "rumors_search",
    should_continue_rumors,
    {
        "continue": "tools",
        "end": END
    }
)
rumors_search_graph.add_edge("tools", "rumors_search")
rumors_graph = rumors_search_graph.compile()

