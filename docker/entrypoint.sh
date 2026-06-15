#!/bin/sh

set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "PostgreSQL is ready"

case "$1" in

  run)
    echo "Starting API..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;

  migrate)
    echo "Running migrations..."
    exec alembic upgrade head
    ;;

  create-admin)
    echo "Creating admin..."
    exec python -m scripts.create_admin
    ;;

  seed)
    echo "Seeding rooms and time slots..."
    exec python -m scripts.rooms_time_slots_init
    ;;

  test)
    echo "Running tests..."
    exec pytest tests -v
    ;;

  *)
    echo "Unknown command: $1"
    echo "Available commands: run | migrate | seed | create-admin"
    exit 1
    ;;

esac