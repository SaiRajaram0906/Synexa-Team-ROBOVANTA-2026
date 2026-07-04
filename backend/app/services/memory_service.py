from ai.memory.memory_manager import MemoryManager
from sqlalchemy.orm import Session

class MemoryService:
    def __init__(self, db: Session):
        self.db = db
        self.memory_manager = MemoryManager()

    def get_business_memory(self, business_id: str):
        # TODO: Retrieve historical timelines and decisions from DB
        return self.memory_manager.load_business_memory(business_id)

    def update_memory(self, business_id: str, memory_data: dict):
        # TODO: Store new executive decisions or KPI outcomes
        return self.memory_manager.append_memory(business_id, memory_data)
