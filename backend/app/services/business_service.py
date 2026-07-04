from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.domain import Business
from uuid import UUID

class BusinessService:
    def __init__(self, db: Session):
        self.repo = BaseRepository(db, Business)
    
    def create_business(self, user_id: str, data: dict):
        data["user_id"] = user_id
        return self.repo.create(data)
        
    def get_business(self, business_id: UUID):
        return self.repo.get_by_id(business_id)
        
    def get_all_businesses(self):
        return self.repo.get_all()
