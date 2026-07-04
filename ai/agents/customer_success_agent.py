from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.prompts.customer_success_prompt import SYSTEM_PROMPT

class CustomerSuccessAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Head of Customer Success",
            goal="Analyze retention risks and predict churn.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
