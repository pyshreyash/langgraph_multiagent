from langchain_core.messages import SystemMessage

def financials_search_prompt(company: str):
    system_prompt = SystemMessage(content=f"""You're an AI assistant running in autonomous mode search financials for the company: {company}""")
    return system_prompt

def news_search_prompt(company: str):
    system_prompt = SystemMessage(content=f"""You're an AI assistant running in autonomous mode search financials for the company: {company}""")
    return system_prompt

def rumors_search_prompt(company: str):
    system_prompt = SystemMessage(content=f"""You're an AI assistant running in autonomous mode search financials for the company: {company}""")
    return system_prompt