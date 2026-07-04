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
        # TODO: Fetch real data from Repositories
        business_profile = {"id": business_id, "name": "TODO", "industry": "TODO"}
        
        # Fetch knowledge and memory
        memory_context = self.memory_service.get_business_memory(business_id)
        knowledge_context = self.knowledge_service.retrieve_context(business_id, "strategic overview")

        return BusinessContext(
            business_id=business_id,
            profile=business_profile,
            goals=[],
            documents_summary="TODO: Summarize doc metadata",
            current_kpis={},
            previous_strategies=[],
            campaign_history=[],
            recommendations=[],
            customer_history={},
            memory_context=memory_context,
            knowledge_context=knowledge_context
        )
