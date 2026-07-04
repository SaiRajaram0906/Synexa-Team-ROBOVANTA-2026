from crewai import Agent
from ai.llm_config import get_gemini_llm

class CEOAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Executive Officer",
            goal="Coordinate business experts, resolve high-level conflicts, and make final executive decisions based on strategic and financial inputs.",
            backstory="A seasoned executive capable of synthesizing inputs from Marketing, Sales, Operations, and Finance to ensure sustainable business growth.",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=[] # TODO: Add tools (e.g., DecisionEngine Tool)
        )
