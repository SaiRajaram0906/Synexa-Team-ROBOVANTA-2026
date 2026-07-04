from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import get_db
from app.services.business_service import BusinessService
from app.middleware.auth import get_current_user

router = APIRouter()

@router.post("/")
def create_business(data: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.create_business(current_user["id"], data)

@router.get("/")
def get_businesses(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.get_all_businesses()

@router.get("/{id}")
def get_business(id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.get_business(id)
