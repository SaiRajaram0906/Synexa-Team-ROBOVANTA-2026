from sqlalchemy.orm import Session
from app.schemas.context import BusinessContext
from app.services.knowledge_service import KnowledgeService
from app.services.memory_service import MemoryService
from app.repositories.base import BaseRepository
from app.models.domain import Business

class BusinessContextService:
    def __init__(self, db: Session):
        self.db = db
        self.business_repo = BaseRepository(db, Business)
        self.knowledge_service = KnowledgeService()
        self.memory_service = MemoryService(db)

    def build_context(self, business_id: str) -> BusinessContext:
        """
        The definitive entry point that constructs the single BusinessContext object
        passed into the CrewAI Executive Crew.
        """
        import uuid
        from app.models.domain import Business, Strategy, KPIMetric
        
        b_uuid = uuid.UUID(business_id) if isinstance(business_id, str) else business_id
        
        # 1. Fetch Business Profile
        business = self.db.query(Business).filter(Business.id == b_uuid).first()
        if not business:
            business_profile = {"id": str(business_id), "name": "Unknown Business", "industry": "SaaS"}
            goals = []
            kpis_dict = {}
        else:
            business_profile = {
                "id": str(business.id),
                "name": business.name,
                "industry": business.industry or "SaaS"
            }
            
            # 2. Fetch Strategy/Goals
            strategy = self.db.query(Strategy).filter(Strategy.business_id == b_uuid).first()
            goals = []
            if strategy and strategy.goals:
                for goal in strategy.goals:
                    if isinstance(goal, dict):
                        goals.append(goal)
                    else:
                        goals.append({"description": str(goal)})
            
            # 3. Fetch KPI Metrics
            kpis = self.db.query(KPIMetric).filter(KPIMetric.business_id == b_uuid).all()
            kpis_dict = {kpi.metric_name: kpi.value for kpi in kpis}
        
        # Fetch knowledge and memory
        memory_context = self.memory_service.get_business_memory(business_id)
        knowledge_context = self.knowledge_service.retrieve_context(business_id, "strategic overview")

        return BusinessContext(
            business_id=str(business_id),
            profile=business_profile,
            goals=goals,
            documents_summary="Demo Document Summary",
            current_kpis=kpis_dict,
            previous_strategies=[],
            campaign_history=[],
            recommendations=[],
            customer_history={},
            memory_context=memory_context,
            knowledge_context=knowledge_context
        )
