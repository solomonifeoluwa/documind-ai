import os
import shutil
import uuid

from sqlalchemy.orm import Session
from app.models.document import Document
from fastapi import HTTPException, UploadFile
from app.core.config import (MAX_UPLOAD_SIZE, ALLOWED_CONTENT_TYPES)

UPLOAD_DIR = "storage/documents"

class DocumentService:
    @staticmethod
    def save_document(
        db: Session, file: UploadFile, owner_id: int
    )-> Document:
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type."
            )

        original_filename = file.filename
        content_type = file.content_type

        extension = os.path.splitext(original_filename)[1]
        stored_filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(UPLOAD_DIR, stored_filename)

        file.file.seek(0, 2)  # Move the file pointer to the end
        file_size = file.file.tell()  # Get the file size
        file.file.seek(0)  # Move the file pointer back to the beginning

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="File cannot be empty."
            )

        if file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the 10 MB limit."
            )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            owner_id=owner_id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document