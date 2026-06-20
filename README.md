Приложение BookRoom Service - Система бронирования комнат с указанием временных интервалов.

1. Установка из репозитория Git
`git clone https://github.com/SumburovSN/meeting-room-booking.git`
`cd BookRoom`

2. Запуск из локального репозитория, созданного Git, с помощью poetry:
* Предварительная подготовка (обязательно):
- применение миграции alembic
`poetry run alembic upgrade head`
- создать admin с данными как в .env.example или .env.docker (ADMIN_EMAIL=admin@bookroom.com ADMIN_PASSWORD=admin123)
`poetry run python -m scripts.create_admin`
- создать admin со своими email и password, например:
`ADMIN_EMAIL="эл. почта" ADMIN_PASSWORD="пароль" poetry run python -m scripts.create_admin`
* Дополнительно можно:
- заполнение таблиц rooms и time_slots данными по умолчанию как в data/rooms.csv:
`poetry run python -m scripts.rooms_time_slots_init`
- наименование полей rooms.csv: room_name,start_time,end_time,slot_minutes
- можно указать путь к своему csv-файлу, например:
`ROOMS_CSV_PATH=путь к my_rooms.csv poetry run python -m scripts.rooms_time_slots_init`
* Запуск приложения (сразу перенаправление на Swagger для удобства проверки):
`poetry run uvicorn app.main:app --reload`
* Запуск тестов
`ENV_FILE=.env.test poetry run pytest tests`

3. Запуск с Docker (Приложение запускается по адресу http://localhost:8000 и сразу перенаправляет на /docs):
С помощью команд Makefile, которые используют docker run
- Build & start API + DB:
`make up`
- Запуск миграций:
`make migrate`
- Создание admin:
`make admin`
Можно со своими данными, например:
`ADMIN_EMAIL=Another.admin@bookroom.com ADMIN_PASSWORD=1 make admin`
- Заполнение данными (rooms + time_slots):
`make seed`
- Посмотреть логи:
`make logs`
- Остановить контейнеры:
`make stop`

- Запуск тестов в полностью изолированном Docker-окружении
`docker compose -f docker-compose.test.yml up --build --abort-on-container-exit`
Команда поднимает:
- отдельный контейнер PostgreSQL для тестов;
- контейнер с приложением и pytest;
- выполняет весь набор тестов;
- автоматически завершает работу после окончания тестирования.

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

6. Бизнес-логика (use cases)
- модель User имеет 4 поля (за исключением id): email, hashed_password, роль (role) и булевое is_active.
Аутентификация осуществляется по email (login) и паролю с созданием JWT токена.
У user 2 роли: admin и employee. Роль admin получается только через скрипт scripts.create_admin. 
Роль employee получается в end-point регистрация.
Предусмотрено только "мягкое" удаление (is_active = false) для сохранения всех бронирований.
Поле email является уникальным, при регистрации и изменении осуществляется проверка на уникальность.
- модель Room имеет 1 поле (за исключением id): name, которое является уникальным. 
При регистрации и изменении осуществляется проверка на уникальность.
- модель TimeSlot имеет 3 поля (за исключением id): связь с Room (room_id), время начала и время окончания. 
При создании нового слота, а также изменении осуществляется проверка на отсутствие пересечения слотов.
- модель Booking создает связи между User и TimeSlot на определенную дату.
При создании осуществляется проверка, чтобы время бронирования было позднее текущего.

7. End points
- /auth/login (post) вход в систему по логину и паролю осуществляется в Swagger либо через соответствующий эндпоинт, 
либо по кнопке Authorize. В поле username вводится email.

- /availability/{date} (get) вывод информации о свободных и занятых слотах на дату для любого пользователя.

- /users (get) вывод всех пользователей только для администратора.
- /users/register (post) ввод нового пользователя только для администратора.
- /users/user_id (put) редактирование пользователя только для администратора, либо самого пользователя.
- /users/user_id (delete) "мягкое" удаление пользователя только для администратора, либо самого пользователя.

- /rooms (get) вывод всех помещений для любого пользователя.
- /rooms (post) создание нового помещения только для администратора.- 
- /rooms/room_id (get) вывод информации о помещении для любого пользователя.
- /rooms/room_id (put) редактирование помещения только для администратора.
- /rooms/room_id (delete) удаление помещения только для администратора (каскадом удаление бронирования).

- /bookings (get) просмотр всех броней только для администратора.
- /bookings (post) бронирование для любого пользователя.
- /bookings/my (get) просмотр брони данного пользователя.
- /bookings/booking_id (delete) удаление брони только для администратора, либо самого пользователя, 
осуществившего бронь.

- /time-slots/room/room_id (get) вывод всех слотов по помещению для любого пользователя.
- /time-slots (post) создание нового слота только для администратора.
- /time-slots/slot_id (put) редактирование слота только для администратора.
- /time-slots/slot_id (delete) удаление слота только для администратора.

Постарался написать код самокомментирующимся.