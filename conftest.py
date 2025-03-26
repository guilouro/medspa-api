import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from database import get_session
from main import app

DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()