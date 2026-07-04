from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/chat")
def chat_copilot(data: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = AIService(db)
    business_id = data.get("business_id") or data.get("businessId") or "00000000-0000-0000-0000-000000000000"
    question = data.get("question") or data.get("message")
    return service.chat_with_copilot(business_id, question)
