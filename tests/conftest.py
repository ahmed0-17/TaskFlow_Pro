
from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.core.database import Base, get_db
from app.core.config import settings

TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/taskflow_pro_test"

test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()




@pytest.fixture
def db_session(test_db):
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
