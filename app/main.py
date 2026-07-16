from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "DocuMind API"}


app.include_router(auth_router)