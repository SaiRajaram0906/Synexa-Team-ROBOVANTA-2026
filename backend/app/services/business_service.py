from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.domain import Business
from uuid import UUID

class BusinessService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(db, Business)
    
    def create_business(self, user_id: str, data: dict):
        import uuid
        from datetime import datetime, timezone
        from app.models.domain import Strategy, KPIMetric
        
        # Extract related data
        kpis = data.pop("kpis", {})
        goals = data.pop("goals", [])
        
        # Format user_id and create business profile
        data["user_id"] = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        business = self.repo.create(data)
        
        # Save KPI metrics
        for k, v in kpis.items():
            if v is not None and v != "":
                kpi = KPIMetric(
                    id=uuid.uuid4(),
                    business_id=business.id,
                    metric_name=k,
                    value=float(v),
                    recorded_at=datetime.now(timezone.utc)
                )
                self.db.add(kpi)
                
        # Save goals into Strategy table
        if goals:
            goals_list = [goals] if isinstance(goals, str) else goals
            strat = Strategy(
                id=uuid.uuid4(),
                business_id=business.id,
                goals=goals_list,
                status="active"
            )
            self.db.add(strat)
            
        self.db.commit()
        return business

    def get_business(self, business_id: UUID):
        return self.repo.get_by_id(business_id)
        
    def get_all_businesses(self):
        return self.repo.get_all()
