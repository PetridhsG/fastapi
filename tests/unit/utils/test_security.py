import pytest
from jose import jwt

from app.api.v1.schemas.auth import TokenData
from app.core.security.jwt import (
    create_access_token,
    credentials_exception,
    verify_access_token,
)
from app.core.security.password import hash_password, verify_password
from tests.conftest import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def test_create_and_verify_access_token():
    data = {"user_id": 123}
    token = create_access_token(data)
    assert isinstance(token, str)

    token_data = verify_access_token(token)
    assert isinstance(token_data, TokenData)
    assert token_data.user_id == 123


def test_verify_access_token_invalid_token():
    invalid_token = "this.is.invalid"

    with pytest.raises(Exception) as exc:
        verify_access_token(invalid_token)

    # JWTError should raise credentials_exception
    assert exc.value.status_code == credentials_exception.status_code
    assert exc.value.detail == credentials_exception.detail


def test_verify_access_token_missing_user_id():

    # Create token without user_id
    token = jwt.encode({"some": "data"}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(Exception) as exc:
        verify_access_token(token)

    assert exc.value.status_code == credentials_exception.status_code
    assert exc.value.detail == credentials_exception.detail


def test_hash_and_verify_password():
    plain = "MyPass123!"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True
    assert verify_password("wrongpass", hashed) is False
