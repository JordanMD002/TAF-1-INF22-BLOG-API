#!/bin/bash
set -e

echo "==> Activation de l'environnement virtuel..."
source .venv/bin/activate

echo "==> Verification des dependances..."
uv pip install -r requirements.txt --quiet

echo "==> Application des migrations..."
python -m alembic upgrade head

echo "==> Lancement du serveur..."
echo ""
echo "  API disponible sur : http://localhost:8000"
echo "  Documentation      : http://localhost:8000/docs"
echo ""
python -m uvicorn main:app --reload