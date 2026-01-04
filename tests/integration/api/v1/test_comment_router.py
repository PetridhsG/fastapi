import pytest  # noqa: F401
from fastapi import status

prefix = "/api/v1/posts"


# -----------------------------
# Create post comment tests
# -----------------------------


def test_create_comment(authorized_client, test_users_with_posts_comments):

    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )
    post_id = test_users_with_posts_comments["user_with_one_post"].posts[0].id

    response = client.post(
        f"{prefix}/{post_id}/comments", json={"content": "This is a test comment."}
    )

    assert response.status_code == status.HTTP_201_CREATED


# -----------------------------
# Get post comments tests
# -----------------------------


def test_get_post_comments(authorized_client, test_users_with_posts_comments):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )
    post_id = test_users_with_posts_comments["user_with_one_post"].posts[0].id

    response = client.get(f"{prefix}/{post_id}/comments")

    assert response.status_code == status.HTTP_200_OK


# -----------------------------
# Update post comment tests
# -----------------------------


def test_update_comment_success(authorized_client, test_users_with_posts_comments):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )

    # Current user commented on this user's post
    post = test_users_with_posts_comments["user_with_one_post"].posts[0]
    comment = post.comments[0]

    response = client.patch(
        f"{prefix}/{post.id}/comments/{comment.id}",
        json={"content": "Updated comment."},
    )

    assert response.status_code == status.HTTP_200_OK


# -----------------------------
# Delete post comment tests
# -----------------------------


def test_delete_comment_success(authorized_client, test_users_with_posts_comments):
    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )

    # Current user commented on this user's post
    post = test_users_with_posts_comments["user_with_one_post"].posts[0]
    comment = post.comments[0]

    response = client.delete(f"{prefix}/{post.id}/comments/{comment.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


# -----------------------------
# General comment tests
# -----------------------------


def test_comment_not_found_general(authorized_client, test_users_with_posts_comments):

    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )

    post = test_users_with_posts_comments["user_with_one_post"].posts[0]

    response = client.patch(
        f"{prefix}/{post.id}/comments/{9999}", json={"content": "Updated comment."}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "comment_not_found"


def test_comment_user_not_allowed_general(
    authorized_client, test_users_with_posts_comments
):

    client = authorized_client.login_as(
        user_email=test_users_with_posts_comments["user_with_two_posts"].email,
        password="Pass123!",
    )

    # Another user commented on this user's post
    post = test_users_with_posts_comments["user_with_two_posts"].posts[0]
    comment = post.comments[0]

    response = client.patch(
        f"{prefix}/{post.id}/comments/{comment.id}",
        json={"content": "Updated comment."},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["error"] == "comment_user_not_allowed"
