#!/bin/bash
set -e

echo "==> Creation de l'environnement virtuel..."
uv venv

echo "==> Installation des dependances..."
source .venv/bin/activate
uv pip install -r requirements.txt

echo "==> Configuration de l'environnement..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  ATTENTION : Remplis le fichier .env avec tes infos MySQL avant de continuer !"
  exit 1
fi

echo "==> Creation de la base de donnees..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS blog_db;"

echo "==> Application des migrations..."
python -m alembic upgrade head

echo ""
echo "  Installation terminee ! Lance ./start.sh pour demarrer."