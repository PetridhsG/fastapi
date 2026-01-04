from os import curdir

import pytest  # noqa: F401
from fastapi import status

from app.api.v1.schemas.post import PostEdit

prefix = "/api/v1/posts"


# -----------------------------
# Create post tests
# -----------------------------
def test_create_post_success(authorized_client):

    post_data = {
        "title": "Test Post",
        "content": "This is a test post content.",
    }

    response = authorized_client.post(f"{prefix}", json=post_data)

    assert response.status_code == status.HTTP_201_CREATED


# -----------------------------
# Get post tests
# -----------------------------


def test_get_post_success(authorized_client, test_users_with_posts):
    post_to_get = test_users_with_posts["user_with_many_posts"].posts[0].id
    response = authorized_client.get(f"{prefix}/{post_to_get}")

    assert response.status_code == status.HTTP_200_OK


def test_get_post_not_found(authorized_client):
    response = authorized_client.get(f"{prefix}/99999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "post_not_found"


# -----------------------------
# Update post tests
# -----------------------------


def test_update_post_success(authorized_client, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="Pass123!"
    )

    post_to_update = current_user.posts[0].id

    response = client.patch(
        f"{prefix}/{post_to_update}",
        json={
            "title": "Updated Title",
            "content": "Updated content for the post.",
        },
    )

    assert response.status_code == status.HTTP_200_OK


# -----------------------------
# Delete post tests
# -----------------------------


def test_delete_post_success(authorized_client, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="Pass123!"
    )

    post_to_delete = current_user.posts[0].id

    response = client.delete(f"{prefix}/{post_to_delete}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


# -----------------------------
# General post tests
# -----------------------------


def test_post_not_found_general(authorized_client, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="Pass123!"
    )

    response = client.patch(
        f"{prefix}/99999",
        json={
            "title": "Updated Title",
            "content": "Updated content for the post.",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "post_not_found"


def test_post_user_not_allowed_general(authorized_client, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]
    target_user = test_users_with_posts["user_with_single_post"]

    client = authorized_client.login_as(
        user_email=current_user.email, password="Pass123!"
    )

    post_to_update = target_user.posts[0].id

    response = client.patch(
        f"{prefix}/{post_to_update}",
        json={
            "title": "Updated Title",
            "content": "Updated content for the post.",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["error"] == "post_user_not_allowed"
