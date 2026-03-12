from langchain_core.messages import SystemMessage
from datetime import datetime, UTC

def financials_search_prompt(company: str):
    prompt = f""" You are AI assistant running in autonomous mode.

                TASK:
                For the given company, determine:
                1. Latest revenue
                2. Latest EBITDA Margin

                RULES:
                - Revenue should be strictly in USD Millions for example: $600 M
                - EBITDA Margin should be strictly in percentage
                - You MUST call the web_search tool to find relevant and updated data as of {datetime.now(UTC).isoformat()}
                - Don't search too much, if no data is available pls return Not available
                - Final answer MUST be derivable from web results
                - Do not hallucinate

                Company: {company}
                """

    return SystemMessage(content=prompt)

def news_search_prompt(company: str):
    prompt = f""" You are AI assistant running in autonomous mode.

            TASK:
            For the given company, determine:
            1. Current and past News that is helpful to judge the Market Sentiment

            RULES:
            - You MUST call the web_search tool to find relevant and updated data as of {datetime.now(UTC).isoformat()}
            - Don't search too much, if no data is available pls return Not available
            - Final answer MUST be derivable from web results
            - Do not hallucinate

            Company: {company}
            """

    return SystemMessage(content=prompt)

def rumors_search_prompt(company: str):
    prompt = f""" You are AI assistant running in autonomous mode.

            TASK:
            For the given company, determine:
            1. Rumors in news and market about the selling of the company

            RULES:
            - You MUST call the web_search tool to find relevant and updated data as of {datetime.now(UTC).isoformat()}
            - Don't search too much, if no data is available pls return Not available
            - Final answer MUST be derivable from web results
            - Do not hallucinate

            Company: {company}
            """
    
    return SystemMessage(content=prompt)