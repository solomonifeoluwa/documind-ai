from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_size: int
    content_type: str
    extracted_text: str | None
    uploaded_at: datetime
    owner_id: int

    model_config = {
        "from_attributes": True,
    }