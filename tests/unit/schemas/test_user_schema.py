import pytest
from pydantic import ValidationError

from app.api.v1.schemas.user import UserCreate


# Helper to create a base valid payload
def valid_user_data(**overrides):
    data = {
        "email": "test@example.com",
        "username": "ValidUser",
        "password": "Pass123!",
        "bio": "Valid bio",
        "is_private": False,
    }
    data.update(overrides)
    return data


# -----------------------------
# Username tests
# -----------------------------


def test_user_create_valid_username():
    user = UserCreate(**valid_user_data(username="ValidUser"))
    assert user.username == "ValidUser"


@pytest.mark.parametrize(
    "username",
    [
        "abc",  # too short
        "a" * 21,  # too long
        "invalid user",  # contains space
    ],
)
def test_user_create_invalid_username(username):
    with pytest.raises(ValidationError):
        UserCreate(**valid_user_data(username=username))


# -----------------------------
# Bio tests
# -----------------------------


def test_user_create_valid_bio():
    user = UserCreate(**valid_user_data(bio="A short bio"))
    assert user.bio == "A short bio"


def test_user_create_bio_optional():
    user = UserCreate(**valid_user_data(bio=None))
    assert user.bio is None


def test_user_create_bio_too_long():
    with pytest.raises(ValidationError):
        UserCreate(**valid_user_data(bio="a" * 201))


# -----------------------------
# Password tests
# -----------------------------


def test_user_create_valid_password():
    user = UserCreate(**valid_user_data(password="Abc123!"))
    assert user.password == "Abc123!"


@pytest.mark.parametrize(
    "password",
    [
        "abc",  # too short
        "abcdefg",  # no uppercase, number, special
        "abcdefG",  # no number, special
        "abcdef1",  # no uppercase, special
        "ABCDEF1",  # no special
    ],
)
def test_user_create_invalid_password(password):
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**valid_user_data(password=password))
    assert (
        "Password must be at least 6 characters long and contain one uppercase letter, one number, and one special character."
        in str(exc_info.value)
    )


# -----------------------------
# Combined happy-path test
# -----------------------------


def test_user_create_all_valid_fields():
    data = valid_user_data(
        username="ValidUser",
        password="Abc123!",
        bio="This is a valid bio",
        is_private=True,
    )
    user = UserCreate(**data)
    assert user.username == data["username"]
    assert user.password == data["password"]
    assert user.bio == data["bio"]
    assert user.is_private is True
