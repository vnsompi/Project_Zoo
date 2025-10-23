FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Installer requirements
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && pip install gunicorn

# Copier le projet
COPY . .

# Créer un utilisateur non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Collecter les fichiers statiques (optionnel)
RUN python manage.py collectstatic --noinput || true

# Commande de démarrage : migrations + lancement serveur
CMD sh -c "python manage.py migrate && gunicorn core.wsgi:application -w 3 -b 0.0.0.0:${PORT:-8000}"

