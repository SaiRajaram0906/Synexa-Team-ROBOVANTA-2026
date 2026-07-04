from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/chat")
def chat_copilot(data: dict, current_user: dict = Depends(get_current_user)):
    service = AIService()
    return service.chat_with_copilot(data.get("business_id"), data.get("message"))
