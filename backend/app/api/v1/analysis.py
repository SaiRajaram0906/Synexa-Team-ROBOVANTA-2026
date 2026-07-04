from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService
import shutil
import os

router = APIRouter()

@router.post("/start")
def start_analysis(business_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = AIService(db)
    return service.run_strategy_agent(business_id)

@router.post("/analyze-dataset")
def analyze_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Create temp directory inside backend
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "temp"))
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        service = AIService(db)
        response = service.run_dataset_analysis(file_path)
        return response
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

@router.get("/{id}")
def get_analysis(id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return analysis results"}
