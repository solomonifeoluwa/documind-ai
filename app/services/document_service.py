import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document

UPLOAD_DIR = "storage/documents"

class DocumentService:
    @staticmethod
    def save_document(
        db: Session, file: UploadFile, owner_id: str
    ):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            title=file.filename,
            filename=filename,
            file_path=file_path,
            owner_id=owner_id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document