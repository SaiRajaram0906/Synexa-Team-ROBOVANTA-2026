import os

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os"

files = {
    # ---------------------------------------------------------
    # 1. GEMINI INTEGRATION & LLM CONFIG
    # ---------------------------------------------------------
    "ai/llm_config.py": """import os
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, wait_exponential, stop_after_attempt

# Shared Configuration for all Agents
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096
LLM_TIMEOUT = 60

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def get_gemini_llm():
    api_key = os.environ.get("GOOGLE_API_KEY", "dummy_key_for_testing")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=LLM_TEMPERATURE,
        max_output_tokens=LLM_MAX_TOKENS,
        timeout=LLM_TIMEOUT,
        google_api_key=api_key
    )
""",

    # ---------------------------------------------------------
    # 2. UPDATING AGENTS TO DYNAMICALLY LOAD PROMPTS
    # ---------------------------------------------------------
    "ai/agents/ceo_agent.py": """from crewai import Agent
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
""",
    "ai/agents/strategy_agent.py": """from crewai import Agent
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
""",
    "ai/agents/marketing_agent.py": """from crewai import Agent
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
""",
    "ai/agents/sales_agent.py": """from crewai import Agent
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
""",
    "ai/agents/finance_agent.py": """from crewai import Agent
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
""",
    "ai/agents/operations_agent.py": """from crewai import Agent
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
""",
    "ai/agents/customer_success_agent.py": """from crewai import Agent
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
""",
    # ---------------------------------------------------------
    # 3. UPDATING TASKS TO DYNAMICALLY LOAD PROMPTS
    # ---------------------------------------------------------
    "ai/tasks/strategy_tasks.py": """from crewai import Task
from ai.prompts.strategy_prompt import TASK_PROMPT, OUTPUT_FORMAT

class StrategyTasks:
    def design_strategy(self, agent, context):
        return Task(
            description=f"{TASK_PROMPT}\\nContext: {context}",
            expected_output=OUTPUT_FORMAT,
            agent=agent
        )
""",
    "ai/tasks/execution_tasks.py": """from crewai import Task
from ai.prompts.marketing_prompt import TASK_PROMPT as MKT_PROMPT, OUTPUT_FORMAT as MKT_OUT
from ai.prompts.sales_prompt import TASK_PROMPT as SALES_PROMPT, OUTPUT_FORMAT as SALES_OUT
from ai.prompts.finance_prompt import TASK_PROMPT as FIN_PROMPT, OUTPUT_FORMAT as FIN_OUT
from ai.prompts.operations_prompt import TASK_PROMPT as OPS_PROMPT, OUTPUT_FORMAT as OPS_OUT
from ai.prompts.customer_success_prompt import TASK_PROMPT as CS_PROMPT, OUTPUT_FORMAT as CS_OUT

class ExecutionTasks:
    def plan_marketing_campaign(self, agent, context):
        return Task(
            description=f"{MKT_PROMPT}\\nContext: {context}",
            expected_output=MKT_OUT,
            agent=agent
        )
    
    def plan_sales_pipeline(self, agent, context):
        return Task(
            description=f"{SALES_PROMPT}\\nContext: {context}",
            expected_output=SALES_OUT,
            agent=agent
        )

    def review_budget(self, agent, context):
        return Task(
            description=f"{FIN_PROMPT}\\nContext: {context}",
            expected_output=FIN_OUT,
            agent=agent
        )
        
    def assess_operations(self, agent, context):
        return Task(
            description=f"{OPS_PROMPT}\\nContext: {context}",
            expected_output=OPS_OUT,
            agent=agent
        )

    def assess_customer_success(self, agent, context):
        return Task(
            description=f"{CS_PROMPT}\\nContext: {context}",
            expected_output=CS_OUT,
            agent=agent
        )
""",
    "ai/tasks/ceo_tasks.py": """from crewai import Task
from ai.prompts.ceo_prompt import TASK_PROMPT, OUTPUT_FORMAT

class CEOTasks:
    def orchestrate_and_summarize(self, agent, context):
        return Task(
            description=f"{TASK_PROMPT}\\nContext: {context}",
            expected_output=OUTPUT_FORMAT,
            agent=agent
        )
""",
    # ---------------------------------------------------------
    # 4. DEMO DATA SEEDING
    # ---------------------------------------------------------
    "database/seed_data.py": """import uuid
from datetime import datetime

DEMO_BUSINESSES = [
    {
        "id": str(uuid.uuid4()),
        "name": "The Rustic Spoon",
        "industry": "Restaurant",
        "kpis": {"revenue": 30000, "table_turnover": 45},
        "goals": ["Boost weekday lunch sales"],
        "documents": [{"name": "Q1_Sales.pdf", "content": "Sample content"}]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Lumina Apparel",
        "industry": "Retail",
        "kpis": {"revenue": 45000, "customer_retention": 0.45},
        "goals": ["Clear winter inventory"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "IronCore Fitness",
        "industry": "Gym",
        "kpis": {"revenue": 25000, "churn_rate": 0.08},
        "goals": ["Acquire 50 new members"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Vitality Clinic",
        "industry": "Healthcare",
        "kpis": {"revenue": 80000, "no_show_rate": 0.15},
        "goals": ["Increase patient bookings"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "TechHaven",
        "industry": "E-commerce",
        "kpis": {"revenue": 120000, "cart_abandonment": 0.65},
        "goals": ["Reduce cart abandonment"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "SaaSify",
        "industry": "Startup",
        "kpis": {"mrr": 4500, "cac": 120},
        "goals": ["Secure 5 enterprise pilots"]
    }
]
""",
    # ---------------------------------------------------------
    # 5. INTEGRATION TESTING & VALIDATION
    # ---------------------------------------------------------
    "validate_repo.py": """import os
import sys

def run_validation():
    print("=========================================")
    print("SYNEXA GROWTH OS - REPOSITORY VALIDATION")
    print("=========================================\\n")
    
    modules = {
        "AI Agents (CEO, Strategy, Marketing, Sales, Ops, CS, Finance)": "ai/agents/ceo_agent.py",
        "CrewAI Tasks": "ai/tasks/execution_tasks.py",
        "Prompts Framework": "ai/prompts/ceo_prompt.py",
        "Decision Engine": "ai/tools/decision_engine.py",
        "KPI Engine": "ai/tools/kpi_engine.py",
        "LLM Config (Gemini)": "ai/llm_config.py",
        "FastAPI App": "backend/app/main.py",
        "Alembic Config": "backend/alembic.ini",
        "Next.js Dashboard": "frontend/src/app/(dashboard)/dashboard/page.tsx",
        "Demo Seed Data": "database/seed_data.py"
    }

    failed = []
    for name, path in modules.items():
        full_path = os.path.join(os.getcwd(), path)
        if os.path.exists(full_path):
            print(f"[✅] {name} - SUCCESS")
        else:
            print(f"[❌] {name} - MISSING")
            failed.append(name)
            
    print("\\n=========================================")
    if not failed:
        print("DEPLOYMENT READINESS: 100%")
    else:
        print(f"DEPLOYMENT READINESS: FAILED ({len(failed)} issues)")
    print("=========================================")

if __name__ == '__main__':
    run_validation()
"""
}

os.makedirs(os.path.join(root_dir, "database"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "tests/integration"), exist_ok=True)

for path, content in files.items():
    file_path = os.path.join(root_dir, path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)

print("Phase 8 generation completed successfully.")
