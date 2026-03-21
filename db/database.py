import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Idéalement, cette URL vient de ton fichier .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Création du moteur de base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour tous nos modèles (Article, User...)
Base = declarative_base()

# Dépendance pour obtenir une session de base de données dans nos routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()