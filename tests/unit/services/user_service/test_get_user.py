import pytest

from app.core.exceptions.user import (
    UserNotFound,
)
from app.services.user_service import UserService

# -----------------------------
# Get public user internal function tests
# -----------------------------


def test_get_public_user_success(user_service: UserService, test_users):
    user = test_users[0]

    user_out = user_service._get_public_user(
        current_user_id=user.id, username=user.username
    )

    assert user_out.id == user.id
    assert user_out.username == user.username


def test_get_public_user_user_is_self(user_service: UserService, test_users):
    user = test_users[0]

    user_out = user_service._get_public_user(
        current_user_id=user.id, username=user.username
    )

    assert user_out.is_following is None


def test_get_public_user_not_found(user_service: UserService, test_users):
    current_user = test_users[0]

    with pytest.raises(UserNotFound):
        user_service._get_public_user(
            current_user_id=current_user.id, username="nonexistent"
        )


# -----------------------------
# Get current user tests
# -----------------------------


def test_get_current_user_success(user_service: UserService, test_users):
    user = test_users[0]

    user_out = user_service.get_current_user(user.id)

    assert user_out.id == user.id
    assert user_out.username == user.username
    assert user_out.is_private is False
    assert user_out.posts_count == 0
    assert user_out.following_count == 0
    assert user_out.followers_count == 0


# -----------------------------
# Get current user settings tests
# -----------------------------


def test_get_current_user_settings_success(user_service: UserService, test_users):
    user = test_users[0]

    user_out = user_service.get_current_user_settings(user.id)

    assert user_out.id == user.id
    assert user_out.username == user.username
    assert user_out.email == user.email
    assert user_out.bio == user.bio
    assert user_out.created_at == user.created_at


# -----------------------------
# Search user tests
# -----------------------------


def test_search_users_found(user_service: UserService, test_users):
    current_user = test_users[0]
    query = "example"

    results = user_service.search_users(current_user.id, query)

    assert len(results) == 2
    for user_out in results:
        assert "example" in user_out.username
        assert user_out.followers_count == 0
        assert user_out.is_following is False


def test_search_users_not_found(user_service: UserService, test_users):
    current_user = test_users[0]
    query = "nonexistent"

    results = user_service.search_users(current_user.id, query)

    assert len(results) == 0
    assert results == []


# -----------------------------
# Get user by username tests
# -----------------------------


def test_get_user_by_username_success(user_service: UserService, test_users):
    current_user = test_users[0]
    user_to_get = test_users[1]

    user_out = user_service.get_user_by_username(current_user.id, user_to_get.username)

    assert user_out.id == user_to_get.id
    assert user_out.username == user_to_get.username
    assert user_out.is_private is True
    assert user_out.posts_count == 0
    assert user_out.following_count == 0
    assert user_out.followers_count == 0
