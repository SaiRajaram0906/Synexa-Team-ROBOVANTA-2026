from .business_memory import BusinessMemory
from .conversation_memory import ConversationMemory

class MemoryManager:
    def __init__(self):
        self.business_memory = BusinessMemory()
        self.conversation_memory = ConversationMemory()

    def load_business_memory(self, business_id: str):
        return self.business_memory.load(business_id)
        
    def append_memory(self, business_id: str, memory_data: dict):
        return self.business_memory.append(business_id, memory_data)
