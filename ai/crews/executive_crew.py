from crewai import Crew, Process
from ai.agents.ceo_agent import CEOAgent
from ai.agents.strategy_agent import StrategyAgent
from ai.agents.marketing_agent import MarketingAgent
from ai.agents.finance_agent import FinanceAgent
from ai.tasks.strategy_tasks import StrategyTasks
from ai.tasks.execution_tasks import ExecutionTasks
from ai.tasks.ceo_tasks import CEOTasks

class ExecutiveCrewManager:
    def __init__(self):
        self.ceo = CEOAgent().create()
        self.strategy = StrategyAgent().create()
        self.marketing = MarketingAgent().create()
        self.finance = FinanceAgent().create()
        
        self.strategy_tasks = StrategyTasks()
        self.exec_tasks = ExecutionTasks()
        self.ceo_tasks = CEOTasks()

    def run_growth_cycle(self, business_context):
        # 1. Define Tasks
        t_strategy = self.strategy_tasks.design_strategy(self.strategy, business_context)
        t_marketing = self.exec_tasks.plan_marketing_campaign(self.marketing, "TODO: inject strategy output")
        t_finance = self.exec_tasks.review_budget(self.finance, "TODO: inject marketing output")
        t_ceo_final = self.ceo_tasks.evaluate_and_approve(self.ceo, "TODO: inject all outputs")

        # 2. Assemble Crew
        crew = Crew(
            agents=[self.strategy, self.marketing, self.finance, self.ceo],
            tasks=[t_strategy, t_marketing, t_finance, t_ceo_final],
            process=Process.sequential, # Can be modified to hierarchical if CEO delegates directly
            verbose=True
        )

        return crew.kickoff()
