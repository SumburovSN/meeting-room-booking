#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is ready"

# -----------------------------
# Command router
# -----------------------------

case "$1" in

  run)
    echo "Starting API..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;

  migrate)
    echo "Running migrations..."
    exec alembic upgrade head
    ;;

  seed)
    echo "Seeding data..."
    python scripts/rooms_time_slots_init.py
    python scripts/create_admin.py
    ;;

  create-admin)
    echo "Creating admin..."
    python -m scripts.create_admin
    ;;

  *)
    echo "Unknown command: $1"
    echo "Available commands: run | migrate | seed | create-admin"
    exit 1
    ;;

esac