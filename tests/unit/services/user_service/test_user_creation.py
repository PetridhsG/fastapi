import pytest

from app.api.v1.schemas.user import UserCreate
from app.core.exceptions.user import (
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.services.user_service import UserService

# -----------------------------
# Create user tests
# -----------------------------


def test_create_user_success(user_service: UserService):
    user_data = UserCreate(
        username="testuser",
        email="test@email.com",
        password="Pass123!",
    )

    user = user_service.create_user(user_data)

    assert user.id is not None
    assert user.email == user_data.email
    assert user.username == user_data.username
    assert user.hashed_password != user_data.password


def test_create_user_with_bio_and_private_flag(user_service: UserService):
    user_data = UserCreate(
        username="privateuser",
        email="private@email.com",
        password="Pass123!",
        bio="My private bio",
        is_private=True,
    )

    user = user_service.create_user(user_data)

    assert user.bio == "My private bio"
    assert user.is_private is True


def test_create_user_duplicate_email(user_service: UserService, test_users):
    existing_user = test_users[0]

    user_data = UserCreate(
        username="newusername",
        email=existing_user.email,
        password="Pass123!",
    )

    with pytest.raises(UserEmailAlreadyExists):
        user_service.create_user(user_data)


def test_create_user_duplicate_username(user_service: UserService, test_users):
    existing_user = test_users[0]

    user_data = UserCreate(
        username=existing_user.username,
        email="new@email.com",
        password="Pass123!",
    )

    with pytest.raises(UsernameAlreadyExists):
        user_service.create_user(user_data)


def test_create_user_duplicate_email_and_username(
    user_service: UserService, test_users
):
    existing_user = test_users[0]

    user_data = UserCreate(
        username=existing_user.username,
        email=existing_user.email,
        password="Pass123!",
    )

    with pytest.raises(UserEmailAlreadyExists):
        user_service.create_user(user_data)
