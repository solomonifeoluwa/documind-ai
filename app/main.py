from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.models.user import User
from app.core.database import Base, engine
from app.api.documents import router as documents_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "DocuMind API"}


app.include_router(auth_router)
app.include_router(documents_router)