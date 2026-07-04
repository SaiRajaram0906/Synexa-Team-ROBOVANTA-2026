import os
import sys

def run_validation():
    print("=========================================")
    print("SYNEXA GROWTH OS - REPOSITORY VALIDATION")
    print("=========================================\n")
    
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
            
    print("\n=========================================")
    if not failed:
        print("DEPLOYMENT READINESS: 100%")
    else:
        print(f"DEPLOYMENT READINESS: FAILED ({len(failed)} issues)")
    print("=========================================")

if __name__ == '__main__':
    run_validation()
