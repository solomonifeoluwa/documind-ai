from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.schemas.user_response import UserResponse
from app.services.auth_service import AuthService, get_auth_service
from app.utils.security import (hash_password, verify_password)
from app.core.security import (create_access_token, get_current_user, verify_access_token)
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"])

@router.get("/test")
def test():
    return {
        "message": "Authentication module is working."
    }

@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)):

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session =Depends(get_db)
):
    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": current_user.phone_number
    }


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
