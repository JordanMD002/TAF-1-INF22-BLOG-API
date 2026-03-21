from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.article_schema import ArticleCreate, ArticleResponse, ArticleUpdate
from services.article_service import ArticleService
from db.database import get_db
from core.deps import get_current_user
from models.user_model import User

router = APIRouter(prefix="/api/articles", tags=["articles"]) 

# 1.GET /articles - Lister tous les articles de l'utilisateur connecté
@router.get("/", response_model=List[ArticleResponse])
async def get_articles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ArticleService.get_all(db, current_user)


# 2. POST /articles - Créer un article
@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ArticleService.create(db, article, current_user)


# 3. GET /articles/{article_id} - Récupérer un article
@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    article = ArticleService.get_by_id(db, article_id, user_id=current_user)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article

 
# 4. PUT /articles/{article_id} - Mise à jour d'un article
@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int, 
    article_update: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_article = ArticleService.update(db, article_id, article_update, user_id=current_user)
    if not updated_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return updated_article


# 5. DELETE /articles/{article_id} - Supprimer un article
@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = ArticleService.delete(db, article_id, user_id=current_user)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return None