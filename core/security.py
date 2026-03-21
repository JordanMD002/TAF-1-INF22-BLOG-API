import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Clé secrète pour signer le token (à mettre dans le .env en production)
SECRET_KEY = os.getenv("SECRET_KEY", "une_cle_super_secrete_pour_le_tp_inf222")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Le token expire dans 1 heure

# Configuration de l'algorithme de hachage (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Vérifie si le mot de passe en clair correspond au hash en base."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Génère un hash à partir d'un mot de passe en clair."""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Génère un nouveau token JWT valide."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Création du token signé
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt