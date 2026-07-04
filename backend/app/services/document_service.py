from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.domain import BusinessDocument
from app.services.knowledge_service import KnowledgeService

class DocumentService:
    def __init__(self, db: Session):
        self.repo = BaseRepository(db, BusinessDocument)
        self.knowledge_service = KnowledgeService()

    def upload_document(self, business_id: str, file_name: str, file_content: bytes):
        # 1. Create DB Record
        doc_record = self.repo.create({
            "business_id": business_id,
            "type": file_name.split('.')[-1],
            "status": "processing"
        })
        
        # 2. Store vectors in Knowledge Layer (ChromaDB)
        self.knowledge_service.process_and_store_document(business_id, file_content, file_name)
        
        # 3. Update DB Record
        doc_record.status = "completed"
        self.repo.db.commit()
        
        return doc_record
