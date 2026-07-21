from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService, get_auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"])

@router.get("/test")
def test():
    return {
        "message": "Authentication module is working."
    }

@router.post("/register")
def register_user(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(user)

@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.get_user(user_id)

@router.get("/search")
def search_users(
    name: str = "Guest",
    auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.search_users(name)

@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    currency: str = "NGN",
    auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.get_product(product_id, currency)   
