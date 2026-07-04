from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/generate")
def generate_strategy(business_id: str, current_user: dict = Depends(get_current_user)):
    service = AIService()
    return service.run_strategy_agent(business_id)

@router.get("/")
def get_strategy(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return generated strategies"}
