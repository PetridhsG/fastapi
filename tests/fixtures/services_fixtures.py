import pytest
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserCreate
from app.services.auth_service import AuthService
from app.services.post_service import PostService
from app.services.user_service import UserService


@pytest.fixture
def auth_service(session: Session) -> AuthService:
    """Provides an AuthService instance with a fresh test session."""
    return AuthService(session)


@pytest.fixture
def user_service(session: Session) -> UserService:
    """Provides a UserService instance with a fresh test session."""
    return UserService(session)


@pytest.fixture
def post_service(session: Session) -> PostService:
    """Provides a PostService instance with a fresh test session."""
    return PostService(session)


@pytest.fixture
def test_users(user_service: UserService):
    """Creates three test users using UserCreate schema."""
    users_data = [
        UserCreate(
            username="exampleUser1", email="user1@example.com", password="User1Pass!"
        ),
        UserCreate(
            username="exampleUser2",
            email="user2@example.com",
            password="User2Pass!",
            bio="This is user 2's bio.",
            is_private=True,
        ),
        UserCreate(
            username="anotheruser3",
            email="user3@example.com",
            password="User3Pass!",
        ),
    ]

    users = [user_service.create_user(u) for u in users_data]
    return users
