from sqlalchemy.orm import Session
from uuid import UUID

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: UUID):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def create(self, obj_in: dict):
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
