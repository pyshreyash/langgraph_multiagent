from langchain_core.tools import tool


@tool
async def tavily_search(query: str) -> str:
    """
    Web Search tool to extract relevant information from the internet"""
    return f"Dummy Tavily async result for: {query}"