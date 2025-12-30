import pytest

from app.api.v1.schemas.user import UserChangePassword, UserEdit
from app.core.exceptions.user import (
    UserInvalidPassword,
    UsernameAlreadyExists,
    UserPasswordUnchanged,
)
from app.services.user_service import UserService

# -----------------------------
# Update user tests
# -----------------------------


def test_update_user_success(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserEdit(
        username="new_username",
        bio="new bio!",
        is_private=True,
    )

    updated_user = user_service.update_user(current_user.id, user_data)

    assert updated_user.username == "new_username"
    assert updated_user.bio == "new bio!"
    assert updated_user.is_private


def test_update_user_username_already_exists(user_service: UserService, test_users):
    current_user = test_users[0]
    existent_username = test_users[1].username
    user_data = UserEdit(
        username=existent_username,
        bio="new bio!",
        is_private=True,
    )

    with pytest.raises(UsernameAlreadyExists):
        user_service.update_user(current_user.id, user_data)


def test_update_user_partial_update(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserEdit(bio="updated bio only")

    updated_user = user_service.update_user(current_user.id, user_data)

    assert updated_user.bio == "updated bio only"
    assert updated_user.username == current_user.username  # unchanged
    assert updated_user.is_private == current_user.is_private  # unchanged


def test_update_user_no_changes(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserEdit()  # all fields None
    updated_user = user_service.update_user(current_user.id, user_data)

    # nothing changed
    assert updated_user.username == current_user.username
    assert updated_user.bio == current_user.bio
    assert updated_user.is_private == current_user.is_private


# -----------------------------
# Change password tests
# -----------------------------


def test_change_password_success(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserChangePassword(
        current_password="User1Pass!",
        new_password="NewPass123!",
    )

    response = user_service.change_password(current_user.id, user_data)
    assert response is None  # change_password returns None on success


def test_change_password_wrong_password(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserChangePassword(
        current_password="invalid-password",
        new_password="NewPass123!",
    )

    with pytest.raises(UserInvalidPassword):
        user_service.change_password(current_user.id, user_data)


def test_change_password_password_unchanged(user_service: UserService, test_users):
    current_user = test_users[0]
    user_data = UserChangePassword(
        current_password="User1Pass!",
        new_password="User1Pass!",
    )

    with pytest.raises(UserPasswordUnchanged):
        user_service.change_password(current_user.id, user_data)


# -----------------------------
# Delete user tests
# -----------------------------


def test_delete_user_success(user_service: UserService, test_users):
    current_user = test_users[0]

    response = user_service.delete_user(current_user.id)
    assert response is None  # delete_user returns None on success
