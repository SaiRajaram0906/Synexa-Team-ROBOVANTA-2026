from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.kpi_service import KPIService

router = APIRouter()

@router.get("")
def get_dashboard_summary(business_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = KPIService(db)
    return service.get_dashboard_data(business_id)
