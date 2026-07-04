from crewai import Agent
from ai.llm_config import get_gemini_llm

class CustomerSuccessAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Head of Customer Success",
            goal="Analyze customer feedback, predict churn, and suggest retention strategies.",
            backstory="A customer-obsessed advocate who believes retention is the true driver of long-term growth.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
