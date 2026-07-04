import os
import textwrap

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os"

files = {
    # ---------------------------------------------------------
    # 1. AI PROMPT FRAMEWORK
    # ---------------------------------------------------------
    "ai/prompts/ceo_prompt.py": """SYSTEM_PROMPT = "TODO: CEO System Prompt"
TASK_PROMPT = "TODO: CEO Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/marketing_prompt.py": """SYSTEM_PROMPT = "TODO: Marketing System Prompt"
TASK_PROMPT = "TODO: Marketing Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/sales_prompt.py": """SYSTEM_PROMPT = "TODO: Sales System Prompt"
TASK_PROMPT = "TODO: Sales Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/finance_prompt.py": """SYSTEM_PROMPT = "TODO: Finance System Prompt"
TASK_PROMPT = "TODO: Finance Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/operations_prompt.py": """SYSTEM_PROMPT = "TODO: Operations System Prompt"
TASK_PROMPT = "TODO: Operations Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/customer_success_prompt.py": """SYSTEM_PROMPT = "TODO: Customer Success System Prompt"
TASK_PROMPT = "TODO: Customer Success Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",
    "ai/prompts/strategy_prompt.py": """SYSTEM_PROMPT = "TODO: Strategy System Prompt"
TASK_PROMPT = "TODO: Strategy Task Instructions"
OUTPUT_FORMAT = "TODO: Expected JSON/Markdown Output Format"
""",

    # ---------------------------------------------------------
    # 3. BUSINESS SCENARIO TESTING
    # ---------------------------------------------------------
    "tests/scenarios/test_scenarios.py": """# Sample Business Scenarios for MVP Demo
SCENARIOS = {
    "retail_store": {
        "profile": {"name": "Lumina Apparel", "industry": "Retail", "type": "B2C"},
        "goals": ["Increase foot traffic by 20%", "Clear winter inventory"],
        "kpis": {"current_revenue": 45000, "customer_retention": 0.45},
        "expected_flow": "Strategy -> Marketing (Local Ads) -> Ops (Inventory) -> Finance (Budget)"
    },
    "restaurant": {
        "profile": {"name": "The Rustic Spoon", "industry": "Food & Beverage", "type": "B2C"},
        "goals": ["Boost weekday lunch sales", "Improve online reviews"],
        "kpis": {"current_revenue": 30000, "table_turnover": 45},
        "expected_flow": "Strategy -> Marketing (Social) -> Customer Success (Reviews) -> Finance"
    },
    "gym": {
        "profile": {"name": "IronCore Fitness", "industry": "Health & Wellness", "type": "B2C"},
        "goals": ["Acquire 50 new members this month", "Reduce churn"],
        "kpis": {"current_revenue": 25000, "churn_rate": 0.08},
        "expected_flow": "Strategy -> Marketing (Promo) -> Sales (Conversion) -> Customer Success"
    },
    "ecommerce": {
        "profile": {"name": "TechHaven", "industry": "E-commerce", "type": "B2C"},
        "goals": ["Increase average order value", "Reduce cart abandonment"],
        "kpis": {"current_revenue": 120000, "cart_abandonment": 0.65},
        "expected_flow": "Strategy -> Marketing (Email Drip) -> Ops (Fulfillment) -> Finance"
    },
    "healthcare": {
        "profile": {"name": "Vitality Clinic", "industry": "Healthcare", "type": "B2C"},
        "goals": ["Increase patient bookings", "Improve patient follow-ups"],
        "kpis": {"current_revenue": 80000, "no_show_rate": 0.15},
        "expected_flow": "Strategy -> Ops (Scheduling) -> Customer Success (Follow-ups) -> Finance"
    },
    "startup": {
        "profile": {"name": "SaaSify", "industry": "Software", "type": "B2B"},
        "goals": ["Secure 5 enterprise pilots", "Achieve $10k MRR"],
        "kpis": {"current_mrr": 4500, "cac": 120},
        "expected_flow": "Strategy -> Marketing (Content) -> Sales (Outreach) -> Finance (Burn Rate)"
    }
}
""",

    # ---------------------------------------------------------
    # 4. SYSTEM LOGGING & MIDDLEWARE
    # ---------------------------------------------------------
    "backend/app/core/logging_config.py": """import logging
import sys

def setup_logging():
    logger = logging.getLogger("synexa_api")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [ReqID: %(request_id)s] - %(message)s'
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
""",

    # ---------------------------------------------------------
    # 9. DOCUMENTATION
    # ---------------------------------------------------------
    "docs/DEPLOYMENT_GUIDE.md": """# Deployment Guide

## 1. Backend (Render)
- Connect repository to Render.
- Set Build Command: `pip install -r backend/requirements.txt`
- Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables required: `DATABASE_URL`, `SUPABASE_JWT_SECRET`, `GOOGLE_API_KEY`.

## 2. Frontend (Vercel)
- Connect repository to Vercel.
- Framework Preset: Next.js
- Root Directory: `frontend`
- Environment Variables required: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_API_URL`.

## 3. Database (Supabase)
- Run Alembic migrations locally with the `DATABASE_URL` pointing to your Supabase Postgres instance.
`cd backend && alembic upgrade head`
""",
    "docs/API_DOCUMENTATION.md": """# API Documentation

## Auth
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`

## Business
- `POST /api/v1/business/`
- `GET /api/v1/business/`

## Documents
- `POST /api/v1/documents/upload`

## Dashboard
- `GET /api/v1/dashboard/`

## Copilot
- `POST /api/v1/copilot/chat`
"""
}

# Create directories
os.makedirs(os.path.join(root_dir, "ai/prompts"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "tests/scenarios"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "docs"), exist_ok=True)

for path, content in files.items():
    file_path = os.path.join(root_dir, path)
    with open(file_path, "w") as f:
        f.write(content)

# UPDATE ai/crews/executive_crew.py for CREWAI CONFIGURATION
crew_path = os.path.join(root_dir, "ai/crews/executive_crew.py")
with open(crew_path, "r") as f:
    crew_content = f.read()

new_crew_config = """        crew = Crew(
            agents=[self.strategy, self.marketing, self.sales, self.finance, self.operations, self.cs, self.ceo],
            tasks=[t_strategy, t_marketing], # TODO: Add all sequential tasks
            process=Process.sequential,
            verbose=True,
            memory=True, # Configured Shared Memory
            max_rpm=100, # API Rate Limiting
            full_output=True # Execution Context
        )"""

crew_content = crew_content.replace(
    """        crew = Crew(
            agents=[self.strategy, self.marketing, self.sales, self.finance, self.operations, self.cs, self.ceo],
            tasks=[t_strategy, t_marketing], # TODO: Add all sequential tasks
            process=Process.sequential,
            verbose=True
        )""",
    new_crew_config
)

with open(crew_path, "w") as f:
    f.write(crew_content)

# UPDATE backend/app/main.py for Logging Middleware
main_path = os.path.join(root_dir, "backend/app/main.py")
with open(main_path, "r") as f:
    main_content = f.read()

middleware_str = """import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging_config import setup_logging
import logging

logger = setup_logging()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        req_id = str(uuid.uuid4())
        start_time = time.time()
        # Inject request_id into logger context in a real app (e.g. using contextvars)
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"[{req_id}] {request.method} {request.url.path} completed in {process_time:.4f}s", extra={"request_id": req_id})
        return response

app.add_middleware(LoggingMiddleware)
"""
if "LoggingMiddleware" not in main_content:
    main_content = main_content.replace('app = FastAPI(title="Synexa Growth OS API")', 'app = FastAPI(title="Synexa Growth OS API")\n' + middleware_str)
    with open(main_path, "w") as f:
        f.write(main_content)

print("Phase 6 implementation completed.")
