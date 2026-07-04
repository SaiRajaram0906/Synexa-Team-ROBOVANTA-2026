from crewai import Agent
from ai.llm_config import get_gemini_llm

class MarketingAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Marketing Officer",
            goal="Design high-converting marketing campaigns based on the overarching business strategy.",
            backstory="An expert marketer who relies on data and trends to acquire new customers efficiently.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[] # TODO: Add tools
        )
