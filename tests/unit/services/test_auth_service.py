from unittest.mock import Mock

import pytest

from app.core.exceptions.auth import InvalidLoginCredentials
from app.services.auth_service import AuthService

# -----------------------------
# Login user tests
# -----------------------------


def test_login_user_success(auth_service, test_users):
    user = test_users[0]

    credentials = Mock()
    credentials.username = user.email
    credentials.password = "User1Pass!"
    result = auth_service.login_user(credentials)

    assert result["access_token"]
    assert result["token_type"] == "bearer"


def test_login_user_email_does_not_exist(auth_service: AuthService):

    credentials = Mock()
    credentials.username = "somerandom@email.com"
    credentials.password = "@Dwd@SD2dsa21"

    with pytest.raises(InvalidLoginCredentials):
        auth_service.login_user(credentials)


def test_login_user_incorrect_password(auth_service: AuthService, test_users):
    user = test_users[0]

    credentials = Mock()
    credentials.username = user.email
    credentials.password = "WrongPassword123!"

    with pytest.raises(InvalidLoginCredentials):
        auth_service.login_user(credentials)
