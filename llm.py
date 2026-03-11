# llm.py
from langchain_openai import ChatOpenAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from tools import tavily_search

def get_llm():

    return ChatNVIDIA(model="openai/gpt-oss-120b").bind_tools([tavily_search])