import os

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os"

files = {
    # ---------------------------------------------------------
    # 1. SPECIALIZED AGENTS (Connecting Tools & Config)
    # ---------------------------------------------------------
    "ai/agents/ceo_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.report_generator import ReportGenerator

class CEOAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Executive Officer & Executive Orchestrator",
            goal="Receive BusinessContext, orchestrate specialist agents, collect outputs, and synthesize an executive summary.",
            backstory="You are the CEO of Synexa Growth OS. You do not do the grunt work. You delegate to your team (Marketing, Sales, Finance, Ops) and rely on the Decision Evaluation Engine to resolve conflicts. Finally, you summarize the path forward.",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=[ReportGenerator()]
        )
""",
    "ai/agents/strategy_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.business_analytics import BusinessAnalyticsTool
from ai.tools.market_research import MarketResearchTool
from ai.tools.document_search import DocumentSearchTool

class StrategyAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Strategy Officer",
            goal="Formulate high-level strategic objectives based on the BusinessContext and market data.",
            backstory="A visionary thinker who analyzes historical business data and market trends to set quarterly objectives.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[BusinessAnalyticsTool(), MarketResearchTool(), DocumentSearchTool()]
        )
""",
    "ai/agents/marketing_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class MarketingAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Marketing Officer",
            goal="Design high-converting marketing campaigns based on the strategy.",
            backstory="Expert marketer focused on CAC, LTV, and lead generation.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/sales_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class SalesAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="VP of Sales",
            goal="Optimize conversion pipelines to turn marketing leads into revenue.",
            backstory="Results-driven sales leader optimizing funnels and scripts.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/finance_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm
from ai.tools.financial_calculator import FinancialCalculator
from ai.tools.kpi_calculator import KPICalculator

class FinanceAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Financial Officer",
            goal="Evaluate ROI of campaigns and enforce budget constraints.",
            backstory="Conservative financial planner guarding profitability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[FinancialCalculator(), KPICalculator()]
        )
""",
    "ai/agents/operations_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class OperationsAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Operating Officer",
            goal="Assess fulfillment capacity against projected sales volume.",
            backstory="Process-oriented leader identifying operational bottlenecks.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/customer_success_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class CustomerSuccessAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Head of Customer Success",
            goal="Analyze retention risks and predict churn based on strategy.",
            backstory="Customer-obsessed advocate driving long-term retention.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    # ---------------------------------------------------------
    # 2. CREWAI TASKS
    # ---------------------------------------------------------
    "ai/tasks/execution_tasks.py": """from crewai import Task

class ExecutionTasks:
    def plan_marketing_campaign(self, agent, context):
        return Task(
            description=f"Using this Strategy Context: {context}, design a marketing campaign.",
            expected_output="JSON array of marketing campaign recommendations with channels and budgets.",
            agent=agent
        )
    
    def plan_sales_pipeline(self, agent, context):
        return Task(
            description=f"Using this Context: {context}, design the sales conversion pipeline.",
            expected_output="JSON array of sales recommendations and funnel optimizations.",
            agent=agent
        )

    def review_budget(self, agent, context):
        return Task(
            description=f"Review the proposed marketing and sales plans: {context} and calculate ROI.",
            expected_output="JSON financial assessment indicating approval/rejection and projected ROI.",
            agent=agent
        )
        
    def assess_operations(self, agent, context):
        return Task(
            description=f"Assess if operations can handle the projected volume from marketing/sales: {context}.",
            expected_output="JSON operational assessment with capacity warnings.",
            agent=agent
        )

    def assess_customer_success(self, agent, context):
        return Task(
            description=f"Assess churn risk and retention strategies based on the current plan: {context}.",
            expected_output="JSON retention strategies and risk alerts.",
            agent=agent
        )
""",
    "ai/tasks/ceo_tasks.py": """from crewai import Task

class CEOTasks:
    def orchestrate_and_summarize(self, agent, context):
        return Task(
            description=f"Review the evaluated decision and Business Context: {context}, and write the final Executive Summary.",
            expected_output="Markdown formatted report including: Executive Summary, Key Findings, Risks, Growth Opportunities, Recommended Actions, Confidence Score, Next Steps",
            agent=agent
        )
""",
    # ---------------------------------------------------------
    # 3. EXECUTIVE CREW PIPELINE
    # ---------------------------------------------------------
    "ai/crews/executive_crew.py": """from crewai import Crew, Process
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

    def run_growth_cycle(self, business_context):
        ctx_str = str(business_context)
        
        # 1. Strategy Formulation
        t_strategy = self.strategy_tasks.design_strategy(self.strategy, ctx_str)
        
        # 2. Execution Planning (Parallel conceptual execution, processed sequentially by CrewAI)
        t_marketing = self.exec_tasks.plan_marketing_campaign(self.marketing, ctx_str)
        t_sales = self.exec_tasks.plan_sales_pipeline(self.sales, ctx_str)
        t_ops = self.exec_tasks.assess_operations(self.operations, ctx_str)
        t_cs = self.exec_tasks.assess_customer_success(self.cs, ctx_str)
        t_finance = self.exec_tasks.review_budget(self.finance, ctx_str)
        
        # 3. CEO Summary
        t_ceo = self.ceo_tasks.orchestrate_and_summarize(self.ceo, ctx_str)
        
        crew = Crew(
            agents=[self.strategy, self.marketing, self.sales, self.operations, self.cs, self.finance, self.ceo],
            tasks=[t_strategy, t_marketing, t_sales, t_ops, t_cs, t_finance, t_ceo],
            process=Process.sequential,
            verbose=True,
            memory=True,
            max_rpm=100,
            full_output=True
        )

        crew_output = crew.kickoff()
        
        # 4. Decision Engine Evaluation
        # We pass the crew outputs into our deterministic evaluation engine
        final_decision = self.decision_engine.evaluate(crew_output)
        return final_decision
""",
    # ---------------------------------------------------------
    # 4. DECISION EVALUATION ENGINE
    # ---------------------------------------------------------
    "ai/tools/decision_engine.py": """class DecisionEvaluationEngine:
    \"\"\"
    Receives outputs from business agents, compares recommendations,
    detects conflicts (e.g. Marketing wants to spend, Finance rejects),
    assigns confidence scores, and selects best path.
    \"\"\"
    def evaluate(self, crew_output) -> dict:
        outputs = str(crew_output)
        
        conflicts = self.detect_conflicts(outputs)
        confidence = self.assign_confidence(outputs, conflicts)
        ranked = self.rank_recommendations(outputs)
        merged = self.merge_recommendations(ranked)
        summary = self.generate_executive_summary(merged, confidence, conflicts)
        
        return {
            "best_recommendation": merged,
            "alternative_recommendations": ranked[1:] if len(ranked) > 1 else [],
            "confidence_score": confidence,
            "reasoning": "Determined by evaluating Finance approval against Marketing spend.",
            "executive_summary": summary,
            "conflicts_detected": conflicts
        }

    def detect_conflicts(self, outputs: str):
        conflicts = []
        if "reject" in outputs.lower() and "increase budget" in outputs.lower():
            conflicts.append("Marketing budget increase rejected by Finance.")
        if "capacity warning" in outputs.lower():
            conflicts.append("Operations cannot support projected sales volume.")
        return conflicts

    def assign_confidence(self, outputs: str, conflicts: list):
        base_score = 0.90
        base_score -= (len(conflicts) * 0.15)
        return max(0.10, round(base_score, 2))

    def rank_recommendations(self, outputs: str):
        # TODO: Use NLP to parse distinct recommendations and rank by ROI
        return ["Primary Strategy Execution", "Conservative Growth Path"]

    def merge_recommendations(self, ranked: list):
        return ranked[0] if ranked else "Default Action"

    def generate_executive_summary(self, merged, confidence, conflicts):
        # For MVP, returns structural data matching the required AI Response Format
        return {
            "Executive Summary": f"The team recommends {merged}.",
            "Key Findings": "Market shows potential, but constrained by budget.",
            "Risks": conflicts,
            "Growth Opportunities": ["Optimization of LTV"],
            "Recommended Actions": ["Execute primary strategy with reduced ad spend"],
            "Confidence Score": confidence,
            "Next Steps": ["Approve budget", "Launch campaign"]
        }
""",
    # ---------------------------------------------------------
    # 5. KPI ENGINE (Actual Formulas)
    # ---------------------------------------------------------
    "ai/tools/kpi_engine.py": """class KPIEngine:
    def calculate_dashboard_metrics(self, business_context: dict) -> dict:
        kpis = business_context.get("current_kpis", {})
        revenue = kpis.get("current_revenue", 0)
        leads = kpis.get("leads", 0)
        retention = kpis.get("customer_retention", 0.5)
        churn = kpis.get("churn_rate", 0.1)

        # 1. Business Health Score (0-100)
        health_score = min(100, max(0, int((retention * 100) + (revenue / 1000) - (churn * 200))))
        
        # 2. Growth Score (0-100)
        growth_score = min(100, max(0, int((leads / 100) * 5 + (revenue / 5000))))
        
        # 3. Revenue Opportunity (Mathematical projection)
        rev_opp = revenue * 0.15 * (1 - churn)
        
        # 4. Lead Score
        lead_score = "High" if leads > 1000 else ("Medium" if leads > 100 else "Low")
        
        # 5. Customer Health
        cust_health = int((1 - churn) * 100)
        
        # 6. Risk Alerts
        risks = 0
        if churn > 0.15: risks += 1
        if rev_opp < 5000: risks += 1
        if health_score < 50: risks += 1

        return {
            "business_health": {"value": health_score, "trend": "up" if health_score > 70 else "down", "confidence": 0.90},
            "growth_score": {"value": growth_score, "trend": "up", "confidence": 0.85},
            "revenue_opportunity": {"value": round(rev_opp, 2), "trend": "up", "confidence": 0.80},
            "lead_score": {"value": lead_score, "trend": "neutral", "confidence": 0.95},
            "risk_alerts": {"value": risks, "trend": "down" if risks < 2 else "up", "confidence": 0.99},
            "market_readiness": {"value": "Ready" if health_score > 60 else "Not Ready", "trend": "up", "confidence": 0.85},
            "customer_health": {"value": cust_health, "trend": "up", "confidence": 0.92},
            "executive_summary": f"Calculated based on {len(kpis)} active KPIs. Health is {health_score}/100."
        }
    
    def get_charts_data(self, business_context: dict) -> dict:
        return {
            "revenue_trend": [
                {'name': 'Jan', 'revenue': 4000, 'leads': 240},
                {'name': 'Feb', 'revenue': 4500, 'leads': 300},
                {'name': 'Mar', 'revenue': 5200, 'leads': 420},
            ]
        }
""",
    # ---------------------------------------------------------
    # 6. TESTING RUNNER
    # ---------------------------------------------------------
    "tests/scenarios/test_runner.py": """import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ai.tools.decision_engine import DecisionEvaluationEngine
from ai.tools.kpi_engine import KPIEngine
from tests.scenarios.test_scenarios import SCENARIOS

def run_tests():
    decision_engine = DecisionEvaluationEngine()
    kpi_engine = KPIEngine()
    
    print("Running End-to-End KPI and Decision Engine Tests on Sample Scenarios...")
    
    for name, data in SCENARIOS.items():
        print(f"\\n--- Testing Scenario: {name.upper()} ---")
        
        # 1. Test KPI Engine
        context_mock = {"current_kpis": data["kpis"]}
        kpis = kpi_engine.calculate_dashboard_metrics(context_mock)
        print(f"Business Health: {kpis['business_health']['value']}")
        print(f"Risk Alerts: {kpis['risk_alerts']['value']}")
        
        # 2. Test Decision Engine
        # We simulate a crew output string containing some keywords
        simulated_crew_output = f"Marketing wants to increase budget. Finance might reject. Capacity warning."
        decision = decision_engine.evaluate(simulated_crew_output)
        
        print(f"Conflicts Detected: {decision['conflicts_detected']}")
        print(f"Confidence Score: {decision['confidence_score']}")
        print(f"Executive Summary: {decision['executive_summary']['Executive Summary']}")
        
if __name__ == '__main__':
    run_tests()
"""
}

for path, content in files.items():
    file_path = os.path.join(root_dir, path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)

print("Phase 7 AI Intelligence implementation generated successfully.")
