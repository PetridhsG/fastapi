import pytest  # noqa: F401
from fastapi import status

prefix = "/api/v1/follows"


# -----------------------------
# Follow user tests
# -----------------------------


def test_follow_user_success(authorized_client, test_users):
    user_to_follow_id = test_users[1].id
    response = authorized_client.post(f"{prefix}/{user_to_follow_id}/follow")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_follow_user_is_self(authorized_client, test_users):
    current_user = test_users[0]
    response = authorized_client.post(f"{prefix}/{current_user.id}/follow")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["error"] == "follow_yourself"


def test_follow_user_already_exists(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow["user1"]
    user_to_follow = test_users_with_follow["user2"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.post(f"{prefix}/{user_to_follow.id}/follow")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "follow_already_exists"


def test_follow_user_not_found(authorized_client):
    response = authorized_client.post(f"{prefix}/99999/follow")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "user_not_found"


# -----------------------------
# Unfollow user / remove follower tests
# -----------------------------


def test_unfollow_user_success(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow["user1"]  # This user follows user2
    user_to_unfollow = test_users_with_follow["user2"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.delete(f"{prefix}/{user_to_unfollow.id}/unfollow")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_follower_success(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow["user2"]  # This user is followed by user1
    follower_user = test_users_with_follow["user1"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User2Pass!"
    )

    response = client.delete(f"{prefix}/{follower_user.id}/follower")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unfollow_follow_not_accepted(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user5"
    ]  # This user sent follow request to user1
    user_to_unfollow = test_users_with_follow["user1"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User5Pass!"
    )

    response = client.delete(f"{prefix}/{user_to_unfollow.id}/unfollow")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["error"] == "follow_not_accepted"


# -----------------------------
# Accept follow tests
# -----------------------------


def test_accept_follow_success(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user1"
    ]  # This user has a follow request from user5
    follower_user = test_users_with_follow["user5"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.patch(f"{prefix}/requests/{follower_user.id}/accept")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_accept_follow_already_accepted(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow["user2"]
    follower_user = test_users_with_follow["user1"]  # This follow is already accepted

    client = authorized_client.login_as(
        user_email=current_user.email, password="User2Pass!"
    )

    response = client.patch(f"{prefix}/requests/{follower_user.id}/accept")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "follow_already_accepted"


# -----------------------------
# Reject/cancel follow tests
# -----------------------------


def test_reject_follow_success(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user1"
    ]  # This user has a follow request from user5
    follower_user = test_users_with_follow["user5"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.delete(f"{prefix}/requests/{follower_user.id}/reject")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_cancel_follow_success(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user1"
    ]  # This user has a follow request from user5
    follower_user = test_users_with_follow["user5"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.delete(f"{prefix}/requests/{follower_user.id}/cancel")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_reject_follow_already_accepted(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow["user2"]
    follower_user = test_users_with_follow["user1"]  # This follow is already accepted

    client = authorized_client.login_as(
        user_email=current_user.email, password="User2Pass!"
    )

    response = client.delete(f"{prefix}/requests/{follower_user.id}/reject")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "follow_already_accepted"


# -----------------------------
# Get follow tests
# -----------------------------


def test_get_incoming_follow_requests(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user1"
    ]  # This user has a follow request from user5

    client = authorized_client.login_as(
        user_email=current_user.email, password="User1Pass!"
    )

    response = client.get(f"{prefix}/requests/incoming")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_outgoing_follow_requests(authorized_client, test_users_with_follow):
    current_user = test_users_with_follow[
        "user5"
    ]  # This user sent a follow request to user1

    client = authorized_client.login_as(
        user_email=current_user.email, password="User5Pass!"
    )

    response = client.get(f"{prefix}/requests/outgoing")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


# -----------------------------
# General follow tests
# -----------------------------


def test_follow_user_is_self_general(authorized_client, test_users):
    # The tests works for many follow related route
    current_user = test_users[0]
    general_route = f"{prefix}/requests/{current_user.id}/accept"

    response = authorized_client.patch(general_route)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["error"] == "follow_yourself"


def test_follow_user_follow_not_found(authorized_client):
    # The tests works for many follow related route
    general_route = f"{prefix}/requests/99999/accept"

    response = authorized_client.patch(general_route)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "follow_not_found"
