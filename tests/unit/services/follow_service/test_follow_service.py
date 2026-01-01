import pytest  # noqa: F401

from app.core.exceptions.follow import (
    FollowAlreadyAccepted,
    FollowAlreadyExists,
    FollowNotAccepted,
    FollowNotFound,
    FollowYourself,
)
from app.db.models.follow import Follow
from app.services.follow_service import FollowService

# -----------------------------
# Get follow internal tests
# -----------------------------


def test_get_follow_success(follow_service: FollowService, test_users_with_follow):
    current_user = test_users_with_follow["user1"]
    user_to_follow = test_users_with_follow["user2"]

    follow = follow_service._get_follow(
        follower_id=current_user.id, followee_id=user_to_follow.id
    )

    assert follow is not None
    assert follow.follower_id == current_user.id
    assert follow.followee_id == user_to_follow.id


def test_get_follow_user_is_self(follow_service: FollowService, test_users):
    current_user = test_users[0]

    with pytest.raises(FollowYourself):
        follow_service._get_follow(
            follower_id=current_user.id, followee_id=current_user.id
        )


def test_get_follow_not_found(follow_service: FollowService):

    with pytest.raises(FollowNotFound):
        follow_service._get_follow(follower_id=9999, followee_id=9998)


# -----------------------------
# Follow user tests
# -----------------------------


def test_follow_user_success(follow_service: FollowService, test_users):
    current_user = test_users[0]
    private_user = test_users[1]

    follow_service.follow_user(follower_id=current_user.id, followee_id=private_user.id)

    follow = follow_service._get_follow(
        follower_id=current_user.id, followee_id=private_user.id
    )
    assert follow is not None
    assert follow.follower_id == current_user.id
    assert follow.followee_id == private_user.id
    # Private users are not auto-accepted
    assert not follow.accepted


def test_follow_user_public_user(session, follow_service: FollowService, test_users):
    current_user = test_users[1]
    public_user = test_users[0]

    follow_service.follow_user(follower_id=current_user.id, followee_id=public_user.id)

    follow = follow_service._get_follow(
        follower_id=current_user.id, followee_id=public_user.id
    )
    assert follow is not None
    assert follow.accepted


def test_follow_user_user_is_self(follow_service: FollowService, test_users):
    current_user = test_users[0]

    with pytest.raises(FollowYourself):
        follow_service.follow_user(
            follower_id=current_user.id, followee_id=current_user.id
        )


def test_follow_user_already_following(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user1"]
    user_to_follow = test_users_with_follow["user2"]

    with pytest.raises(FollowAlreadyExists):
        follow_service.follow_user(
            follower_id=current_user.id, followee_id=user_to_follow.id
        )


# -----------------------------
# Unfollow user tests
# -----------------------------


def test_unfollow_user_success(
    session, follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user1"]
    user_to_unfollow = test_users_with_follow["user2"]

    follow_service.unfollow_user(
        follower_id=current_user.id, followee_id=user_to_unfollow.id
    )

    follow = session.get(Follow, (current_user.id, user_to_unfollow.id))
    assert follow is None


def test_unfollow_follow_not_accepted(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user5"]
    user_to_unfollow = test_users_with_follow["user1"]

    with pytest.raises(FollowNotAccepted):
        follow_service.unfollow_user(
            follower_id=current_user.id, followee_id=user_to_unfollow.id
        )


# -----------------------------
# Accept follow tests
# -----------------------------


def test_accept_follow_success(follow_service: FollowService, test_users_with_follow):
    current_user = test_users_with_follow["user1"]
    follower_user = test_users_with_follow["user5"]  # This user sent the follow request

    follow_service.accept_follow_request(
        follower_id=follower_user.id, followee_id=current_user.id
    )

    follow = follow_service._get_follow(
        follower_id=follower_user.id, followee_id=current_user.id
    )

    assert follow.accepted


def test_accept_follow_already_accepted(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user2"]
    follower_user = test_users_with_follow["user1"]

    with pytest.raises(FollowAlreadyAccepted):
        follow_service.accept_follow_request(
            follower_id=follower_user.id, followee_id=current_user.id
        )


# -----------------------------
# Reject follow tests
# -----------------------------


def test_reject_follow_success(follow_service: FollowService, test_users_with_follow):
    current_user = test_users_with_follow["user1"]
    follower_user = test_users_with_follow["user5"]  # This user sent the follow request

    follow_service.reject_follow_request(
        follower_id=follower_user.id, followee_id=current_user.id
    )

    with pytest.raises(FollowNotFound):
        follow_service._get_follow(
            follower_id=follower_user.id, followee_id=current_user.id
        )


def test_reject_follow_already_accepted(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user2"]
    follower_user = test_users_with_follow["user1"]

    with pytest.raises(FollowAlreadyAccepted):
        follow_service.reject_follow_request(
            follower_id=follower_user.id, followee_id=current_user.id
        )


# -----------------------------
# Get follow tests
# -----------------------------


def test_get_incoming_follow_requests(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user6"]

    requests = follow_service.get_follow_requests(
        user_id=current_user.id, incoming=True
    )
    assert len(requests) == 1
    follower_ids = {req.follower_id for req in requests}
    assert test_users_with_follow["user5"].id in follower_ids


def test_get_incoming_follow_requests_no_requests(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user4"]

    requests = follow_service.get_follow_requests(
        user_id=current_user.id, incoming=True
    )

    assert len(requests) == 0
    assert requests == []


def test_get_outgoing_follow_requests(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user5"]

    requests = follow_service.get_follow_requests(
        user_id=current_user.id, incoming=False
    )

    assert len(requests) == 2
    followee_ids = {req.followee_id for req in requests}
    assert test_users_with_follow["user1"].id in followee_ids
    assert test_users_with_follow["user6"].id in followee_ids


def test_get_outgoing_follow_requests_no_requests(
    follow_service: FollowService, test_users_with_follow
):
    current_user = test_users_with_follow["user4"]

    requests = follow_service.get_follow_requests(
        user_id=current_user.id, incoming=False
    )

    assert len(requests) == 0
    assert requests == []
