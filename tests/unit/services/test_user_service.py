import pytest  # noqa: F401

from app.api.v1.schemas.user import UserChangePassword, UserCreate, UserEdit
from app.core.exceptions.user import (
    UserEmailAlreadyExists,
    UserInvalidPassword,
    UsernameAlreadyExists,
    UserNotFound,
    UserPasswordUnchanged,
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


# -----------------------------
# Get user followers tests
# -----------------------------


def test_get_user_followers_target_has_followers(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user3"]
    current_user = test_users_with_follow["user4"]

    followers = user_service.get_user_followers(
        current_user_id=current_user.id, target_user_id=target_user.id
    )
    # Extract the usernames to ensure no ordering issues
    followers_usernames = {user.username for user in followers}

    expected_usernames = {"user1", "user2"}  # User1 follows these

    assert followers_usernames == expected_usernames
    assert len(followers) == 2


def test_get_user_followers_target_has_followers_with_search(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user3"]
    current_user = test_users_with_follow["user4"]

    followers = user_service.get_user_followers(
        current_user_id=current_user.id, target_user_id=target_user.id, search="user1"
    )

    # Extract the usernames to ensure no ordering issues
    followers_usernames = {user.username for user in followers}

    expected_usernames = {"user1"}  # User1 follows these

    assert followers_usernames == expected_usernames
    assert len(followers) == 1


def test_get_user_followers_target_has_followers_with_search_no_results(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user3"]
    current_user = test_users_with_follow["user4"]

    followers = user_service.get_user_followers(
        current_user_id=current_user.id,
        target_user_id=target_user.id,
        search="non-existent-user",
    )

    assert followers == []
    assert len(followers) == 0


def test_get_user_followers_target_has_no_followers(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user1"]
    current_user = test_users_with_follow["user4"]

    followers = user_service.get_user_followers(
        current_user_id=current_user.id, target_user_id=target_user.id
    )

    assert len(followers) == 0


# -----------------------------
# Get user following tests
# -----------------------------


def test_get_user_following_target_has_followings(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user1"]
    current_user = test_users_with_follow["user4"]

    following = user_service.get_user_following(
        current_user_id=current_user.id, target_user_id=target_user.id
    )
    # Extract the usernames to ensure no ordering issues
    following_usernames = {user.username for user in following}

    expected_usernames = {"user2", "user3"}  # User1 follows these

    assert following_usernames == expected_usernames
    assert len(following) == 2


def test_get_user_following_target_has_followings_with_search(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user1"]
    current_user = test_users_with_follow["user4"]

    following = user_service.get_user_following(
        current_user_id=current_user.id, target_user_id=target_user.id, search="user2"
    )

    # Extract the usernames to ensure no ordering issues
    following_usernames = {user.username for user in following}

    expected_usernames = {"user2"}  # User1 follows these

    assert following_usernames == expected_usernames
    assert len(following) == 1


def test_get_user_following_target_has_followings_with_search_no_results(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user1"]
    current_user = test_users_with_follow["user4"]

    following = user_service.get_user_following(
        current_user_id=current_user.id,
        target_user_id=target_user.id,
        search="non-existent-user",
    )

    assert following == []
    assert len(following) == 0


def test_get_user_following_target_has_no_followings(
    user_service: UserService, test_users_with_follow
):
    target_user = test_users_with_follow["user3"]
    current_user = test_users_with_follow["user4"]

    following = user_service.get_user_following(
        current_user_id=current_user.id, target_user_id=target_user.id
    )

    assert following == []
    assert len(following) == 0
