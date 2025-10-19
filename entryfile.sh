#!/usr/bin/env bash
set -e

# Attendre la DB si DB_HOST est défini
if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  until python - <<PY
import sys, psycopg2, os
try:
    psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", "5432"),
        connect_timeout=3
    )
except Exception:
    sys.exit(1)
PY
  do
    sleep 1
  done
  echo "Database is up!"
fi

python manage.py migrate
python manage.py collectstatic --noinput || true

# ✅ Lancer le serveur en production avec Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3