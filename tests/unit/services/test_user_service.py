import pytest

from app.api.v1.schemas.user import UserCreate
from app.core.exceptions.user import UserEmailAlreadyExists, UserNotFound
from app.services.user_service import UserService


def test_create_user_success(user_service: UserService):
    user_data = UserCreate(email="test@email.com", password="Pass123!")
    user = user_service.create_user(user_data)
    assert user.id is not None
    assert user.email == user_data.email
    assert user.hashed_password != user_data.password


def test_create_user_duplicate_email(user_service: UserService, test_users):
    existing_user = test_users[0]
    user_data = UserCreate(email=existing_user.email, password="NewPass123!")
    with pytest.raises(UserEmailAlreadyExists):
        user_service.create_user(user_data)


def test_get_user_success(user_service: UserService, test_users):
    existing_user = test_users[0]
    user = user_service.get_user(existing_user.id)
    assert user.id == existing_user.id
    assert user.email == existing_user.email


def test_get_user_not_found(user_service: UserService):
    with pytest.raises(UserNotFound):
        user_service.get_user(999999)
