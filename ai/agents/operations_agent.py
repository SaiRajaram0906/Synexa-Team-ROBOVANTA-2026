from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.prompts.operations_prompt import SYSTEM_PROMPT

class OperationsAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Operating Officer",
            goal="Assess fulfillment capacity against projected sales volume.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
