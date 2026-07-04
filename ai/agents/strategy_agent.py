from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.business_analytics import BusinessAnalyticsTool
from ai.tools.market_research import MarketResearchTool
from ai.tools.document_search import DocumentSearchTool
from ai.prompts.strategy_prompt import SYSTEM_PROMPT

class StrategyAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Strategy Officer",
            goal="Formulate high-level strategic objectives.",
            backstory=SYSTEM_PROMPT,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[BusinessAnalyticsTool(), MarketResearchTool(), DocumentSearchTool()]
        )
