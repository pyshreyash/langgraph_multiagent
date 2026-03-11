from pydantic import BaseModel

class Financials(BaseModel):
    revenue: str
    ebitda_margin: str

class Sentiment(BaseModel):
    news_summary: str

class Rumors(BaseModel):
    sell_rumor: str


class DiscoveryOutput(BaseModel):
    financials: Financials
    sentiment: Sentiment
    rumors: Rumors

class Scores(BaseModel):
    financials_score: int
    sentiment_score: int
    willingness_to_sell: int

