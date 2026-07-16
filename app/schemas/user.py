from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)