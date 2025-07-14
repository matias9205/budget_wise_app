import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session
from sqlalchemy.orm import sessionmaker

from app.config.db import db
from app.config.config import settings
from app.main import app
from app.users.models import User

engine = create_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)
print(f"CONNECTED TO {engine.url} DATABASE")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    db.Base.metadata.create_all(bind=engine)
    yield
    db.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[db.get_db] = override_get_db
    with TestClient(app) as c:
        yield c