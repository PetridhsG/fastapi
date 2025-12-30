import pytest  # noqa: F401

from app.services.user_service import UserService

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
