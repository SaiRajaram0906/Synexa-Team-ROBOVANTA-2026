from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/upload")
async def upload_document(
    business_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = DocumentService(db)
    content = await file.read()
    doc = service.upload_document(business_id, file.filename, content)
    return {"document_id": doc.id, "status": doc.status}
