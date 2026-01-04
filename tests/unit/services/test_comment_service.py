import pytest

from app.api.v1.schemas.comment import CommentCreate
from app.core.exceptions.comment import CommentNotFound, CommentUserNotAllowed
from app.services.comment_service import CommentService  # noqa: F401

# -----------------------------
# Get post comment internal function tests
# -----------------------------


def test_get_comment_for_a_post_success(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]
    user2 = test_users_with_posts_comments["user_with_one_post"]

    # user1 commented on user2's post
    post = user2.posts[0]
    comment = post.comments[0]

    result = comment_service._get_comment(
        current_user_id=user1.id,
        post_id=post.id,
        comment_id=comment.id,
    )

    assert result.id == comment.id
    assert result.owner_id == user1.id
    assert result.post_id == post.id


def test_get_comment_for_a_post_not_found(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]
    user2 = test_users_with_posts_comments["user_with_one_post"]

    post = user2.posts[0]

    with pytest.raises(CommentNotFound):
        comment_service._get_comment(
            current_user_id=user1.id,
            post_id=post.id,
            comment_id=9999,
        )


def test_get_comment_for_a_post_user_not_allowed(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]

    post = user1.posts[0].comments[0]
    comment = user1.posts[0].comments[0]  # This is user's 2 comments

    with pytest.raises(CommentUserNotAllowed):
        comment_service._get_comment(
            current_user_id=user1.id,
            post_id=post.id,
            comment_id=comment.id,
        )


# -----------------------------
# Create post comment tests
# -----------------------------


def test_create_comment(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]

    comment = comment_service.add_post_comment(
        current_user_id=user1.id,
        post_id=user1.posts[0].id,
        comment_create=CommentCreate(content="Test comment"),
    )

    assert comment.content == "Test comment"
    assert comment.owner_id == user1.id


# -----------------------------
# Get post comments tests
# -----------------------------


def test_get_post_comments(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]

    comments = comment_service.get_post_comments(
        current_user_id=user1.id,
        post_id=user1.posts[0].id,
    )

    assert len(comments) == 2


# -----------------------------
# Update post comment tests
# -----------------------------


def test_update_comment_success(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]
    user2 = test_users_with_posts_comments["user_with_one_post"]
    post = user2.posts[0]
    comment = post.comments[0]

    updated_comment = comment_service.update_post_comment(
        current_user_id=user1.id,
        post_id=post.id,
        comment_id=comment.id,
        comment_update=CommentCreate(content="Updated comment"),
    )

    assert updated_comment.content == "Updated comment"


# -----------------------------
# Delete post comment tests
# -----------------------------


def test_delete_comment_success(
    comment_service: CommentService, test_users_with_posts_comments
):
    user1 = test_users_with_posts_comments["user_with_two_posts"]
    user2 = test_users_with_posts_comments["user_with_one_post"]
    post = user2.posts[0]
    comment = post.comments[0]

    deleted_comment = comment_service.delete_post_comment(
        current_user_id=user1.id,
        post_id=post.id,
        comment_id=comment.id,
    )

    assert deleted_comment is None
