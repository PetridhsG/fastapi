import pytest  # noqa: F401

from app.api.v1.schemas.post import PostCreate, PostEdit
from app.core.exceptions.post import PostNotFound, PostUserNotAllowed
from app.services.post_service import PostService

# -----------------------------
# Get user posts internal function tests
# -----------------------------


def test_get_post_for_a_user_success(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    post = post_service._get_post_for_user(
        current_user_id=current_user.id,
        post_id=current_user.posts[0].id,
    )
    assert post.id == current_user.posts[0].id


def test_get_post_for_a_user_not_found(
    post_service: PostService, test_users_with_posts
):
    current_user = test_users_with_posts["user_with_many_posts"]

    with pytest.raises(PostNotFound):
        post_service._get_post_for_user(
            current_user_id=current_user.id,
            post_id=9999,
        )


def test_get_post_for_a_user_not_owner(
    post_service: PostService, test_users_with_posts
):
    current_user = test_users_with_posts["user_without_posts"]
    other_user = test_users_with_posts["user_with_many_posts"]

    with pytest.raises(PostUserNotAllowed):
        post_service._get_post_for_user(
            current_user_id=current_user.id,
            post_id=other_user.posts[0].id,
        )


# -----------------------------
# Create post tests
# -----------------------------


def test_create_post_success(post_service: PostService, test_users):
    current_user = test_users[0]
    post_data = PostCreate(
        title="Test Post",
        content="This is a test post content.",
    )

    post = post_service.create_post(
        current_user_id=current_user.id, post_create=post_data
    )
    assert post.id is not None
    assert post.title == post_data.title
    assert post.content == post_data.content
    assert post.owner_id == current_user.id


# -----------------------------
# Get user posts tests
# -----------------------------


def test_get_user_posts_success(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    posts = post_service.get_user_posts(
        current_user_id=current_user.id, target_user_id=current_user.id
    )
    assert len(posts) == 3
    for post in posts:
        assert post.owner_id == current_user.id


def test_get_user_posts_no_posts(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_without_posts"]

    posts = post_service.get_user_posts(
        current_user_id=current_user.id, target_user_id=current_user.id
    )
    assert len(posts) == 0


# -----------------------------
# Get post tests
# -----------------------------


def test_get_post_success(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]
    target_post = current_user.posts[0]

    post = post_service.get_post(
        current_user_id=current_user.id, post_id=target_post.id
    )
    assert post.id == target_post.id
    assert post.title == target_post.title
    assert post.content == target_post.content
    assert post.owner.id == current_user.id
    assert post.comments_count == 0


def test_get_post_not_found(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]

    with pytest.raises(PostNotFound):
        post_service.get_post(current_user_id=current_user.id, post_id=9999)


# -----------------------------
# Update post tests
# -----------------------------


def test_update_post_success(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]
    target_post = current_user.posts[0]

    post_update = PostEdit(
        title="Updated Title",
        content="Updated content for the post.",
    )

    updated_post = post_service.update_post(
        current_user_id=current_user.id,
        post_id=target_post.id,
        post_update=post_update,
    )

    assert updated_post.id == target_post.id
    assert updated_post.title == post_update.title
    assert updated_post.content == post_update.content


# -----------------------------
# Delete post tests
# -----------------------------


def test_delete_post_success(post_service: PostService, test_users_with_posts):
    current_user = test_users_with_posts["user_with_many_posts"]
    target_post = current_user.posts[0]

    post_service.delete_post(
        current_user_id=current_user.id,
        post_id=target_post.id,
    )

    with pytest.raises(PostNotFound):
        post_service.get_post(
            current_user_id=current_user.id,
            post_id=target_post.id,
        )
