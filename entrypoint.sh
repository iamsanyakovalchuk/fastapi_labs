#!/bin/sh

set -e

# Тут в Лабі №4 ми додамо команду: alembic upgrade head
echo "Запуск сервера FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload