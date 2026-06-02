from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.core.config import settings


# Engine (sync вариант под psycopg2)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # проверяет соединение перед использованием
    echo=False            # True можно включить для дебага SQL
)


# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


# Base class для моделей SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass