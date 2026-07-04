from crewai import Agent
from ai.llm_config import get_gemini_llm

class FinanceAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Financial Officer",
            goal="Evaluate ROI of proposed campaigns, enforce budget constraints, and manage financial risk.",
            backstory="A conservative financial planner who ensures that growth does not come at the cost of profitability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
