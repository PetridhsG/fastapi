import pytest
from fastapi.testclient import TestClient
from pydantic_settings import SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.database import Base, get_db
from app.main import app
from tests.fixtures.services_fixtures import *  # noqa: F403


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")


# Load test settings
settings = TestSettings()

# Create engine and session for test DB
SQLALCHEMY_DATABASE_URL = settings.database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="function")
def session():
    """
    Drops all tables and recreates them for a fresh test database
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    """
    TestClient that uses the fresh session
    """

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def authorized_client(client, test_users):
    """
    TestClient with default logged-in user (test_users[0]),
    but also supports manual login via a callable.
    """

    # Default login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_users[0].email,
            "password": "User1Pass!",
        },
    )
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})

    # Also allow manual login
    def _get(user_email: str, password: str):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": user_email, "password": password},
        )
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        return client

    client.login_as = _get  # attach the callable to client
    return client
