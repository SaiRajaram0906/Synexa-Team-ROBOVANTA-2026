from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.report_generator import ReportGenerator
from ai.prompts.ceo_prompt import SYSTEM_PROMPT

class CEOAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Executive Officer",
            goal="Orchestrate specialist agents and synthesize an executive summary.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=[ReportGenerator()]
        )
