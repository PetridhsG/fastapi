import pytest  # noqa: F401
from fastapi import status

from app.core.enums import ReactionType

prefix = "/api/v1/posts"

# -----------------------------
# Create post reaction tests
# -----------------------------


def test_create_reaction(authorized_client, test_users_with_posts_reactions):

    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )

    post_id = test_users_with_posts_reactions["user_with_two_posts"].posts[0].id

    response = client.post(
        f"{prefix}/{post_id}/reactions", json={"type": ReactionType.fire}
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_reaction_already_exists(
    authorized_client, test_users_with_posts_reactions
):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )
    # User already reacted
    post_id = test_users_with_posts_reactions["user_with_one_post"].posts[0].id

    response = client.post(
        f"{prefix}/{post_id}/reactions", json={"type": ReactionType.fire}
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["error"] == "reaction_already_exists"


# -----------------------------
# Get post reactions tests
# -----------------------------


def test_get_post_reactions(authorized_client, test_users_with_posts_reactions):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )
    post_id = test_users_with_posts_reactions["user_with_two_posts"].posts[0].id

    response = client.get(f"{prefix}/{post_id}/reactions")

    assert response.status_code == status.HTTP_200_OK


# -----------------------------
# Update post reaction tests
# -----------------------------


def test_update_reaction_success(authorized_client, test_users_with_posts_reactions):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )

    # User reacted to this post
    post_id = test_users_with_posts_reactions["user_with_one_post"].posts[0].id

    response = client.patch(
        f"{prefix}/{post_id}/reactions", json={"type": ReactionType.fire}
    )

    assert response.status_code == status.HTTP_200_OK


# -----------------------------
# Delete post reaction tests
# -----------------------------


def test_delete_reaction_success(authorized_client, test_users_with_posts_reactions):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )

    # User reacted to this post
    post_id = test_users_with_posts_reactions["user_with_one_post"].posts[0].id

    response = client.delete(f"{prefix}/{post_id}/reactions")

    assert response.status_code == status.HTTP_204_NO_CONTENT


# -----------------------------
# General reaction tests
# -----------------------------


def test_reaction_not_found_general(authorized_client, test_users_with_posts_reactions):

    client = authorized_client.login_as(
        user_email=test_users_with_posts_reactions["user_with_two_posts"].email,
        password="Pass123!",
    )

    # User not reacted to this post
    post_id = test_users_with_posts_reactions["user_with_two_posts"].posts[0].id

    response = client.patch(
        f"{prefix}/{post_id}/reactions", json={"type": ReactionType.fire}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "reaction_not_found"
