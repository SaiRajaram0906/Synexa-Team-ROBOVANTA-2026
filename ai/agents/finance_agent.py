from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.financial_calculator import FinancialCalculator
from ai.tools.kpi_calculator import KPICalculator
from ai.prompts.finance_prompt import SYSTEM_PROMPT

class FinanceAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Financial Officer",
            goal="Evaluate ROI of campaigns and enforce budget constraints.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[FinancialCalculator(), KPICalculator()]
        )
