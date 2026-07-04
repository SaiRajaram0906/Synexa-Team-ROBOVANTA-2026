from crewai import Agent
from ai.llm_config import get_gemini_llm

class SalesAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="VP of Sales",
            goal="Optimize conversion pipelines and design sales scripts to turn leads into revenue.",
            backstory="A results-driven sales leader focused on closing deals and optimizing the sales funnel.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
