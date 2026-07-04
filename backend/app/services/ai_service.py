from app.services.business_context_service import BusinessContextService
from ai.crews.executive_crew import ExecutiveCrewManager
from ai.tools.decision_engine import DecisionEvaluationEngine
from sqlalchemy.orm import Session

class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.context_service = BusinessContextService(db)
        self.crew_manager = ExecutiveCrewManager()
        self.decision_engine = DecisionEvaluationEngine()

    def run_strategy_agent(self, business_id: str):
        import json
        from ai.tools.kpi_engine import KPIEngine
        
        # 1. Build context
        context = self.context_service.build_context(business_id)
        
        # 2. Multi-agent cycle
        decision = self.crew_manager.run_growth_cycle(context)
        print(f"[LOG] Decision Engine output: {json.dumps(decision, indent=2)}")
        
        # 3. Pass decision to KPI Engine
        kpi_engine = KPIEngine()
        kpi_output = kpi_engine.calculate_scores_from_decision(decision, context.model_dump())
        print(f"[LOG] KPI Engine output: {json.dumps(kpi_output, indent=2)}")
        
        final_response = {
            "status": "success",
            "decision": decision,
            "kpi_metrics": kpi_output
        }
        print(f"[LOG] Final API response: {json.dumps(final_response, indent=2)}")
        return final_response
        
    def chat_with_copilot(self, business_id: str, message: str):
        """
        The definitive Copilot workflow:
        User Question -> Context Builder -> Crew -> Decision Engine -> Response
        """
        # 1. Context Retrieval
        context = self.context_service.build_context(business_id)
        
        # 2. Executive Crew processes the question against context
        decision = self.crew_manager.run_growth_cycle(context, user_question=message)
        
        # 3. Final output
        return {"response": decision["final_strategy"], "reasoning": decision["executive_summary"]}

    def run_dataset_analysis(self, file_path: str):
        import json
        from app.services.dataset_service import DatasetService
        from ai.tools.kpi_engine import KPIEngine
        
        # 1. Process dataset
        dataset_service = DatasetService()
        context = dataset_service.process_csv_dataset(file_path)
        
        # 2. Run multi-agent Crew cycle
        decision = self.crew_manager.run_growth_cycle(context)
        print(f"[LOG] Decision Engine output: {json.dumps(decision, indent=2)}")
        
        # 3. Pass decision to KPI Engine
        kpi_engine = KPIEngine()
        kpi_output = kpi_engine.calculate_scores_from_decision(decision, context.model_dump())
        charts_output = kpi_engine.get_charts_data(context.model_dump())
        print(f"[LOG] KPI Engine output: {json.dumps(kpi_output, indent=2)}")
        
        # 4. Extract agent specific insights for AI Insights section
        agent_outputs = decision.get("all_agent_outputs", [])
        
        ceo_out = next((ao for ao in agent_outputs if ao.get("agent") == "CEO"), {})
        mkt_out = next((ao for ao in agent_outputs if ao.get("agent") == "Marketing"), {})
        sales_out = next((ao for ao in agent_outputs if ao.get("agent") == "Sales"), {})
        fin_out = next((ao for ao in agent_outputs if ao.get("agent") == "Finance"), {})
        ops_out = next((ao for ao in agent_outputs if ao.get("agent") == "Operations"), {})
        cs_out = next((ao for ao in agent_outputs if ao.get("agent") == "CustomerSuccess"), {})
        strat_out = next((ao for ao in agent_outputs if ao.get("agent") == "Strategy"), {})
        
        # Collect all risks
        all_risks = []
        for ao in agent_outputs:
            if ao.get("risks"):
                all_risks.extend(ao.get("risks"))
                
        ai_insights = {
            "executive_summary": decision.get("executive_summary", "Synthesis complete."),
            "key_business_insights": ceo_out.get("findings", ["Optimizing dataset variables."]),
            "marketing_insights": mkt_out.get("findings", []) + mkt_out.get("recommendations", []),
            "sales_insights": sales_out.get("findings", []) + sales_out.get("recommendations", []),
            "finance_insights": fin_out.get("findings", []) + fin_out.get("recommendations", []),
            "operations_insights": ops_out.get("findings", []) + ops_out.get("recommendations", []),
            "customer_success_insights": cs_out.get("findings", []) + cs_out.get("recommendations", []),
            "risks_identified": all_risks if all_risks else ["None identified."],
            "growth_opportunities": strat_out.get("recommendations", []),
            "final_strategic_recommendation": decision.get("final_strategy", "")
        }
        
        # 5. Persist this business context to the database so that it's selectable!
        from app.models.domain import Business, KPIMetric, Strategy
        import uuid
        from datetime import datetime, timezone
        
        biz_id = uuid.uuid4()
        business = Business(
            id=biz_id,
            name="Uploaded CSV Dataset",
            industry="General Retail",
            profile_summary="Dataset-derived business context",
            user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(business)
        
        # Add KPIs
        for metric, val_dict in kpi_output.items():
            if isinstance(val_dict, dict) and "value" in val_dict:
                val = val_dict["value"]
                if isinstance(val, str):
                    val = 100.0 if val in ["High", "Ready"] else 50.0
                kpi_row = KPIMetric(
                    id=uuid.uuid4(),
                    business_id=biz_id,
                    metric_name=metric,
                    value=float(val),
                    recorded_at=datetime.now(timezone.utc)
                )
                self.db.add(kpi_row)
                
        # Add Strategy
        strat = Strategy(
            id=uuid.uuid4(),
            business_id=biz_id,
            goals=[g["description"] for g in context.goals],
            status="active"
        )
        self.db.add(strat)
        self.db.commit()
        
        final_response = {
            "status": "success",
            "business_id": str(biz_id),
            "metrics": kpi_output,
            "charts": charts_output,
            "ai_insights": ai_insights
        }
        
        print(f"[LOG] Final API response for dataset: {json.dumps(final_response, indent=2)}")
        return final_response
