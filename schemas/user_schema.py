from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, description="Nom d'utilisateur (3-50 caracteres)")
    password: str = Field(..., min_length=6, description="Mot de passe (minimum 6 caracteres)")

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.strip():
            raise ValueError("Le nom d'utilisateur ne peut pas etre vide")
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, - et _")
        return v.strip().lower()

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caracteres")
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str