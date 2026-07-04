from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_dashboard_summary(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return high level dashboard stats"}

@router.get("/kpis")
def get_kpis(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return KPI metrics"}
