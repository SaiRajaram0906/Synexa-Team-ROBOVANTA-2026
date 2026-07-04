from crewai import Agent
from ai.llm_config import get_gemini_llm

class StrategyAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Strategy Officer",
            goal="Formulate quarterly and annual strategic objectives based on market analysis and business capabilities.",
            backstory="A visionary thinker who maps out the long-term direction of the business.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
