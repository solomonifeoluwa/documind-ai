from fastapi import APIRouter
from app.schemas.user import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"])

@router.get("/test")
def test():
    return {
        "message": "Authentication module is working."
    }

@router.post("/register")
def register_user(user: UserCreate):
    return {
        "message": "User registered successfully.",
        "user": {
            "full_name": user.full_name,
            "email": user.email
        }
    }

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
    }

@router.get("/search")
def search_users(name: str = "Guest"):
    return {
        "search":name
    }

@router.get("/products/{product_id}")
def get_product(product_id: int, currency: str = "NGN"):
    return {
        "product_id": product_id,
        "currency": currency
    }
