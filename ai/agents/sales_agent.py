from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.prompts.sales_prompt import SYSTEM_PROMPT

class SalesAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="VP of Sales",
            goal="Optimize conversion pipelines to turn marketing leads into revenue.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
