
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


# Database Engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)


# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base Class for Database Models
class Base(DeclarativeBase):
    pass


# Database Dependency
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
