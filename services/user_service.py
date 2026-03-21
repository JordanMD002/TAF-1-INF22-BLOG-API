from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate
from core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    def create_user(db: Session, user_in: UserCreate):
        hashed_pw = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_pw,
            role=user_in.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user