from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from jose import jwt
from pytest_mock import mocker  # noqa: F401

from app.api.v1.schemas.auth import TokenData
from app.core.exceptions.auth import AuthInvalidJWT
from app.core.exceptions.user import UserNotAllowedToViewResource, UserNotFound
from app.core.security.access_controls import can_view_target_user, get_current_user
from app.core.security.jwt import (
    create_access_token,
    verify_access_token,
)
from app.core.security.password import hash_password, verify_password
from app.db.models.user import User
from tests.conftest import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def make_mock_db(user=None, follow_exists=None):
    db = Mock()
    # Mock user query
    db.query().filter().first.side_effect = [user, follow_exists]
    return db


# -----------------------------
# JWT Tests
# -----------------------------


def test_create_and_verify_access_token():
    data = {"user_id": 123}
    token = create_access_token(data)
    assert isinstance(token, str)

    token_data = verify_access_token(token)
    assert isinstance(token_data, TokenData)
    assert token_data.user_id == 123


def test_verify_access_token_invalid_token():
    invalid_token = "this.is.invalid"

    with pytest.raises(AuthInvalidJWT) as exc:
        verify_access_token(invalid_token)

    assert exc.value.status_code == 401
    assert exc.value.error == "invalid_jwt"


def test_verify_access_token_missing_user_id():
    # Create token without user_id
    token = jwt.encode({"some": "data"}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(AuthInvalidJWT) as exc:
        verify_access_token(token)

    assert exc.value.status_code == 401
    assert exc.value.error == "invalid_jwt"


# -----------------------------
# Password Tests
# -----------------------------


def test_hash_and_verify_password():
    plain = "MyPass123!"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True
    assert verify_password("wrongpass", hashed) is False


# -----------------------------
# Get curent user Tests
# -----------------------------


def test_get_current_user_success(mocker):  # noqa: F811
    fake_token_data = SimpleNamespace(user_id=1)

    mocker.patch(
        "app.core.security.access_controls.verify_access_token",
        return_value=fake_token_data,
    )

    fake_user = User(id=1, email="x@test.com", hashed_password="x")
    db = Mock()
    db.get.return_value = fake_user

    result = get_current_user(token="fake", db=db)

    assert result == fake_user


def test_get_current_user_not_found(mocker):  # noqa: F811
    fake_token_data = SimpleNamespace(user_id=1)

    mocker.patch(
        "app.core.security.access_controls.verify_access_token",
        return_value=fake_token_data,
    )

    db = Mock()
    db.get.return_value = None

    with pytest.raises(UserNotFound):
        get_current_user(token="fake", db=db)


# -----------------------------
# Can view target user Tests
# -----------------------------


def test_target_user_not_found():
    db = make_mock_db(user=None)
    current_user = SimpleNamespace(id=1)
    with pytest.raises(UserNotFound):
        can_view_target_user(username="unknown", db=db, current_user=current_user)


def test_target_user_public():
    public_user = SimpleNamespace(id=2, is_private=False)
    db = make_mock_db(user=public_user)
    current_user = SimpleNamespace(id=1)

    result = can_view_target_user(username="public", db=db, current_user=current_user)
    assert result == public_user


def test_target_user_is_current_user():
    private_user = SimpleNamespace(id=1, is_private=True)
    db = make_mock_db(user=private_user)
    current_user = SimpleNamespace(id=1)

    result = can_view_target_user(username="private", db=db, current_user=current_user)
    assert result == private_user


def test_target_user_private_followed():
    private_user = SimpleNamespace(id=2, is_private=True)
    follow = SimpleNamespace()
    db = make_mock_db(user=private_user, follow_exists=follow)
    current_user = SimpleNamespace(id=1)

    result = can_view_target_user(username="private", db=db, current_user=current_user)
    assert result == private_user


def test_target_user_private_not_followed():
    private_user = SimpleNamespace(id=2, is_private=True)
    db = make_mock_db(user=private_user, follow_exists=None)
    current_user = SimpleNamespace(id=1)

    with pytest.raises(UserNotAllowedToViewResource):
        can_view_target_user(username="private", db=db, current_user=current_user)
