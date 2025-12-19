import pytest
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService


@pytest.fixture
def user_service(session: Session) -> UserService:
    """Provides a UserService instance with a fresh test session."""
    return UserService(session)


@pytest.fixture
def auth_service(session: Session) -> AuthService:
    """Provides an AuthService instance with a fresh test session."""
    return AuthService(session)


@pytest.fixture
def test_users(user_service: UserService):
    """Creates three test users using UserCreate schema."""
    users_data = [
        UserCreate(email="user1@example.com", password="User1Pass!"),
        UserCreate(email="user2@example.com", password="User2Pass!"),
        UserCreate(email="user3@example.com", password="User3Pass!"),
    ]

    users = [user_service.create_user(u) for u in users_data]
    return users
