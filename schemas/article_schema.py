from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    titre: str = Field(..., min_length=1, max_length=200, description="Titre de l'article (obligatoire)")
    contenu: str = Field(..., min_length=1, description="Contenu de l'article (obligatoire)")
    auteur: str = Field(..., min_length=1, max_length=100, description="Nom de l'auteur (obligatoire)")
    categorie: Optional[str] = Field(None, max_length=100, description="Categorie de l'article")
    tags: Optional[str] = Field(None, max_length=255, description="Tags separes par des virgules")

    @field_validator('titre')
    @classmethod
    def titre_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Le titre ne peut pas etre vide ou contenir uniquement des espaces")
        return v.strip()

    @field_validator('auteur')
    @classmethod
    def auteur_not_blank(cls, v):
        if not v.strip():
            raise ValueError("L'auteur ne peut pas etre vide")
        return v.strip()

    @field_validator('contenu')
    @classmethod
    def contenu_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Le contenu ne peut pas etre vide")
        return v.strip()

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    titre: Optional[str] = Field(None, min_length=1, max_length=200)
    contenu: Optional[str] = Field(None, min_length=1)
    auteur: Optional[str] = Field(None, min_length=1, max_length=100)
    categorie: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=255)

    @field_validator('titre')
    @classmethod
    def titre_not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Le titre ne peut pas etre vide")
        return v.strip() if v else v

class ArticleResponse(ArticleBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True