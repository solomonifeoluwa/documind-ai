from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.services.document_service import DocumentService
from app.models.user import User
from app.schemas.document import DocumentResponse  

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post("/uploads", response_model=DocumentResponse)

def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   return DocumentService.save_document(db=db, file=file, owner_id=current_user.id)