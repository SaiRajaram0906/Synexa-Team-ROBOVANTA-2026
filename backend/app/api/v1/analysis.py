from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/start")
def start_analysis(business_id: str, current_user: dict = Depends(get_current_user)):
    # TODO: Implement trigger for analysis workflow
    return {"status": "started"}

@router.get("/{id}")
def get_analysis(id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return analysis results"}
