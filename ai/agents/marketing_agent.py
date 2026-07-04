from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.prompts.marketing_prompt import SYSTEM_PROMPT

class MarketingAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Marketing Officer",
            goal="Design high-converting marketing campaigns.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
