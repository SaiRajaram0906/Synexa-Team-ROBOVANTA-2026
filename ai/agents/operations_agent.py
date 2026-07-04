from crewai import Agent
from ai.llm_config import get_gemini_llm

class OperationsAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Operating Officer",
            goal="Ensure fulfillment capacity can handle projected sales volume and identify operational bottlenecks.",
            backstory="A process-oriented leader who ensures that the business can deliver on its promises to customers.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
