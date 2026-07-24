from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.models.user import User
from app.core.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "DocuMind API"}


app.include_router(auth_router)