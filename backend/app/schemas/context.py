from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class BusinessContext(BaseModel):
    business_id: str
    profile: Dict[str, Any]
    goals: List[Dict[str, Any]]
    documents_summary: str
    current_kpis: Dict[str, Any]
    previous_strategies: List[Dict[str, Any]]
    campaign_history: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    customer_history: Dict[str, Any]
    memory_context: str
    knowledge_context: str
