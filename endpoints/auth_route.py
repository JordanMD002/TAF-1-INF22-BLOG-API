from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from db.database import get_db
from core.security import create_access_token
from services.user_service import UserService
from schemas.user_schema import Token, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserService.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    
    return {
        "access_token": create_access_token(subject=user.email),
        "token_type": "bearer",
    }