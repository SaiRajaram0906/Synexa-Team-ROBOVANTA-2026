from crewai import Crew, Process
from ai.agents.ceo_agent import CEOAgent
from ai.agents.strategy_agent import StrategyAgent
from ai.agents.marketing_agent import MarketingAgent
from ai.agents.sales_agent import SalesAgent
from ai.agents.finance_agent import FinanceAgent
from ai.agents.operations_agent import OperationsAgent
from ai.agents.customer_success_agent import CustomerSuccessAgent
from ai.tasks.strategy_tasks import StrategyTasks
from ai.tasks.execution_tasks import ExecutionTasks
from ai.tasks.ceo_tasks import CEOTasks
from ai.tools.decision_engine import DecisionEvaluationEngine

class ExecutiveCrewManager:
    def __init__(self):
        self.ceo = CEOAgent().create()
        self.strategy = StrategyAgent().create()
        self.marketing = MarketingAgent().create()
        self.sales = SalesAgent().create()
        self.finance = FinanceAgent().create()
        self.operations = OperationsAgent().create()
        self.cs = CustomerSuccessAgent().create()
        
        self.strategy_tasks = StrategyTasks()
        self.exec_tasks = ExecutionTasks()
        self.ceo_tasks = CEOTasks()
        
        self.decision_engine = DecisionEvaluationEngine()

    def run_growth_cycle(self, business_context, user_question=None):
        import json
        
        # 1. Print BusinessContext received
        context_dict = business_context.model_dump() if hasattr(business_context, "model_dump") else business_context
        goals = context_dict.get("goals", [])
        goals_desc = goals[0].get("description", "Optimize business metrics") if (goals and isinstance(goals[0], dict)) else (goals[0] if goals else "Optimize business metrics")
        
        actual_question = user_question or f"Generate business strategy for goal: {goals_desc}"
        
        print(f"[LOG] Incoming Question: {actual_question}")
        print(f"[LOG] Business Context: {json.dumps(context_dict, indent=2)}")
        
        # 2. Run CEO Agent: analyzes business objective and decides which specialist agents to execute
        print("[LOG] Agent execution started: Chief Executive Officer")
        biz_name = context_dict.get("profile", {}).get("name", "the business")
        industry = context_dict.get("profile", {}).get("industry", "SaaS")
        
        print(f"[LOG] CEO analyzing business objective for {biz_name}: '{goals_desc}'")
        
        # CEO Decides which specialist agents should execute
        specialists = ["Marketing", "Sales", "Finance", "Operations", "CustomerSuccess"]
        print(f"[LOG] CEO decided that all specialist agents should execute: {specialists}")
        
        ceo_output = {
            "agent": "CEO",
            "summary": f"Orchestrated analysis for {biz_name} in {industry} industry to address goal: '{goals_desc}'.",
            "findings": [f"Targeting objective: {goals_desc}."],
            "recommendations": [f"Trigger execution cycle for specialists: {', '.join(specialists)}."],
            "risks": ["Coordination complexity across multiple department agents."],
            "confidence": 0.95
        }
        print(f"[LOG] Agent output: {json.dumps(ceo_output, indent=2)}")
        print("[LOG] Agent execution completed: Chief Executive Officer")

        # 3. Execution of specialist agents
        task_ctx = {
            "profile": context_dict.get("profile", {}),
            "goals": goals,
            "current_kpis": context_dict.get("current_kpis", {}),
            "user_question": actual_question
        }
        ctx_str = str(task_ctx)
        
        t_strategy = self.strategy_tasks.design_strategy(self.strategy, ctx_str)
        t_marketing = self.exec_tasks.plan_marketing_campaign(self.marketing, ctx_str)
        t_sales = self.exec_tasks.plan_sales_pipeline(self.sales, ctx_str)
        t_ops = self.exec_tasks.assess_operations(self.operations, ctx_str)
        t_cs = self.exec_tasks.assess_customer_success(self.cs, ctx_str)
        t_finance = self.exec_tasks.review_budget(self.finance, ctx_str)
        t_ceo = self.ceo_tasks.orchestrate_and_summarize(self.ceo, ctx_str)
        
        crew = Crew(
            agents=[self.strategy, self.marketing, self.sales, self.operations, self.cs, self.finance, self.ceo],
            tasks=[t_strategy, t_marketing, t_sales, t_ops, t_cs, t_finance, t_ceo],
            process=Process.sequential,
            verbose=True
        )

        try:
            crew_output = crew.kickoff()
        except Exception as e:
            print(f"[ERROR] Agent execution failed: {str(e)}")
            raise RuntimeError(f"Agent execution failed: {str(e)}")
            
        crew_output["CEO"] = ceo_output
        agent_outputs_list = list(crew_output.values())
        
        # 4. Decision Evaluation Engine receives ALL agent outputs
        print(f"[LOG] Decision Engine input: {json.dumps(agent_outputs_list, indent=2)}")
        
        final_decision = self.decision_engine.evaluate(agent_outputs_list, business_context)
        print(f"[LOG] Decision Engine Output: {json.dumps(final_decision, indent=2)}")
        print(f"[LOG] Final Response: {final_decision['final_strategy']}")
        
        return final_decision
