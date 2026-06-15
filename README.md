Приложение BookRoom Service - Система бронирования комнат с указанием временных интервалов.

1. Установка из репозитория Git
git clone https://github.com/SumburovSN/meeting-room-booking.git
cd BookRoom

2. Запуск из локального репозитория, созданного Git, с помощью poetry:
Предварительная подготовка (обязательно):
- применение миграции alembic
poetry run alembic upgrade head
- создать admin с данными как в .env.example или .env.docker (ADMIN_EMAIL=admin@bookroom.com ADMIN_PASSWORD=admin123)
poetry run python -m scripts.create_admin
- создать admin со своими email и password, например:
ADMIN_EMAIL="эл. почта" ADMIN_PASSWORD="пароль" poetry run python -m scripts.create_admin
Дополнительно можно:
- заполнение таблиц rooms и time_slots данными по умолчанию как в data/rooms.csv:
poetry run python -m scripts.rooms_time_slots_init
- наименование полей rooms.csv: room_name,start_time,end_time,slot_minutes
- можно указать путь к своему csv-файлу, например:
ROOMS_CSV_PATH=путь к my_rooms.csv poetry run python -m scripts.rooms_time_slots_init
Запуск приложения (сразу перенаправление на Swagger для удобства проверки):
poetry run uvicorn app.main:app --reload
Запуск тестов
ENV_FILE=.env.test poetry run pytest tests

3. Запуск с Docker (Приложение запускается по адресу http://localhost:8000):
- Build & start API + DB:
make up
- Запуск миграций:
make migrate
- Создание admin:
make admin
- Заполнение данными (rooms + time_slots):
make seed
- Запуск тестов
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit


4. Использованные технологии:
- Python 3.12
- Poetry
- FastAPI 
- PostgreSQL 17
- SQLAlchemy
- Alembic
- Docker + Docker Compose
- Pytest

5. Архитектура проекта
- Слой Domain + Persistence: models;
- Слой Application (use cases - бизнес логика): services;
- Слой Infrastructure: repositories, core;
- Слой Presentation: api, schemas;
- Composition Root: main.py
