import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.core.config import settings
from app.dependencies.db import get_db
from app.models.user import User, UserRole
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.core.security import hash_password, create_access_token
from datetime import time


assert "bookroom_test" in settings.DATABASE_URL, (
    f"Tests are using non-test database: {settings.DATABASE_URL}"
)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def employee_user(db_session):
    user = User(
        email="employee@test.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def admin_auth_headers(admin_user):
    token = create_access_token(
        admin_user.id,
        admin_user.role.value,
    )

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def auth_headers(employee_user):
    token = create_access_token(
        employee_user.id,
        employee_user.role.value,
    )

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def room(db_session):
    room = Room(
        name="Room A"
    )

    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    return room


@pytest.fixture
def time_slot(db_session, room):
    slot = TimeSlot(
        room_id=room.id,
        start_time=time(9, 0),
        end_time=time(10, 0),
    )

    db_session.add(slot)
    db_session.commit()
    db_session.refresh(slot)

    return slot


@pytest.fixture
def employee_user_2(db_session):
    user = User(
        email="employee2@test.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user
