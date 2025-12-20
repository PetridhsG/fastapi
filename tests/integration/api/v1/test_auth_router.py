import pytest  # noqa: F401
from fastapi import status

# -----------------------------
# Login user tests
# -----------------------------


def test_login_success(client, test_users):
    user = test_users[0]

    response = client.post(
        "/api/v1/login",
        data={
            "username": user.email,
            "password": "User1Pass!",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_email(client):
    response = client.post(
        "/api/v1/login",
        data={"username": "wrong@example.com", "password": "any"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"]["error"] == "invalid_login_credentials"


def test_login_invalid_password(client, test_users):
    user = test_users[0]

    response = client.post(
        "/api/v1/login",
        data={"username": user.email, "password": "WrongPass!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"]["error"] == "invalid_login_credentials"
