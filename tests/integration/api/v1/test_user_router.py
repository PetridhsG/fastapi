import pytest  # noqa: F401
from fastapi import status

from app.api.v1.schemas.user import UserCreatedOut

prefix = "/api/v1/users"

# -----------------------------
# Create user tests
# -----------------------------


def test_create_user_success(client):

    response = client.post(
        prefix,
        json={
            "username": "test_user",
            "email": "test_email@email.com",
            "password": "Qwerty12!",
        },
    )

    new_user = UserCreatedOut(**response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert new_user.username == "test_user"
    assert new_user.email == "test_email@email.com"


def test_create_user_existing_email(client, test_users):

    existing_user = test_users[0]

    response = client.post(
        prefix,
        json={
            "username": "new_username",
            "email": existing_user.email,
            "password": "Qwerty12!",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "user_email_already_exists"


def test_create_user_existing_username(client, test_users):

    existing_user = test_users[0]

    response = client.post(
        prefix,
        json={
            "username": existing_user.username,
            "email": "new_email@email.com",
            "password": "Qwerty12!",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "username_already_exists"


# -----------------------------
# Get current user tests
# -----------------------------


def test_get_current_user_success(authorized_client, test_users):
    user = test_users[0]
    response = authorized_client.get(f"{prefix}/me")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user.username


# -----------------------------
# Get current user settings tests
# -----------------------------


def test_get_current_user_settings_success(authorized_client, test_users):
    user = test_users[0]
    response = authorized_client.get(f"{prefix}/me/settings")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user.username
    assert response.json()["is_private"] == user.is_private


# -----------------------------
# Search user tests
# -----------------------------


def test_search_users_success(authorized_client, test_users):
    user = test_users[0]
    query = user.username[:3]
    response = authorized_client.get(f"{prefix}?query={query}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


def test_search_users_no_results(authorized_client, test_users):

    query = "no-match-string"
    response = authorized_client.get(f"{prefix}?query={query}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


# -----------------------------
# Get user by username tests
# -----------------------------


def test_get_user_by_username(authorized_client, test_users):
    user = test_users[0]

    response = authorized_client.get(f"{prefix}/{user.username}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user.username
    assert response.json()["is_private"] == user.is_private


def test_get_user_by_username_not_found(authorized_client):

    response = authorized_client.get(f"{prefix}/{'non_existent_user'}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "user_not_found"


# -----------------------------
# Get user followers tests
# -----------------------------


def test_get_user_followers_route(authorized_client, test_users_with_follow):
    target_user = test_users_with_follow["user3"]
    response = authorized_client.get(f"{prefix}/{target_user.username}/followers")

    assert response.status_code == status.HTTP_200_OK

    followers = response.json()
    assert any(follower["username"] == "user1" for follower in followers)


# -----------------------------
# Get user following tests
# -----------------------------


def test_get_user_following_route(authorized_client, test_users_with_follow):
    target_user = test_users_with_follow["user1"]
    response = authorized_client.get(f"{prefix}/{target_user.username}/following")

    assert response.status_code == status.HTTP_200_OK

    followers = response.json()
    assert any(follower["username"] == "user2" for follower in followers)


# -----------------------------
# Get user posts tests
# -----------------------------


def test_get_user_posts_route(authorized_client, user_with_posts):
    user = user_with_posts
    response = authorized_client.get(f"{prefix}/{user.username}/posts")

    assert response.status_code == status.HTTP_200_OK
    posts = response.json()

    assert len(posts) == 2

    titles = [post["title"] for post in posts]
    assert "Post 1" in titles


# -----------------------------
# Update user tests
# -----------------------------


def test_update_user_success(authorized_client):
    new_data = {
        "username": "updated_username",
        "bio": "Updated bio",
    }
    response = authorized_client.patch(f"{prefix}/me", json=new_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == new_data["username"]
    assert response.json()["bio"] == new_data["bio"]


def test_update_user_username_exists(authorized_client, test_users_with_follow):

    response = authorized_client.patch(
        f"{prefix}/me",
        json={"username": test_users_with_follow["user1"].username},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "username_already_exists"


# -----------------------------
# Change password tests
# -----------------------------


def test_change_password_success(authorized_client):
    new_password_data = {
        "current_password": "User1Pass!",
        "new_password": "NewPass123!",
    }
    response = authorized_client.put(
        f"{prefix}/me/password",
        json=new_password_data,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current(authorized_client):
    new_password_data = {
        "current_password": "WrongPass!",
        "new_password": "NewPass123!",
    }
    response = authorized_client.put(
        f"{prefix}/me/password",
        json=new_password_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["error"] == "invalid_password"


def test_change_password_unchanged(authorized_client):
    new_password_data = {
        "current_password": "User1Pass!",
        "new_password": "User1Pass!",
    }
    response = authorized_client.put(
        f"{prefix}/me/password",
        json=new_password_data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "password_unchanged"


# -----------------------------
# Delete user tests
# -----------------------------

def test_delete_user_success(authorized_client):
    response = authorized_client.delete(f"{prefix}/me")
    assert response.status_code == status.HTTP_204_NO_CONTENT

# -----------------------------
# Access control router tests
# -----------------------------


def test_get_resource_unauthorized(client, test_users):
    target_user = test_users[0]
    response = client.get(f"{prefix}/{target_user.username}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_resource_forbidden(authorized_client, test_users_with_follow):
    private_user = test_users_with_follow["user4"]
    response = authorized_client.get(f"{prefix}/{private_user.username}/followers")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["error"] == "user_not_allowed_to_view_resource"
