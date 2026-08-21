from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    id: str
    title: str
    filename: str
    owner_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }