import pytest

from app.api.v1.schemas.reaction import ReactionCreate, ReactionEdit
from app.core.enums import ReactionType
from app.core.exceptions.reaction import ReactionAlreadyExists, ReactionNotFound
from app.services.reaction_service import ReactionService

# -----------------------------
# Get reaction internal function tests
# -----------------------------


def test_get_reaction_for_a_post_success(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user1 = test_users_with_posts_reactions["user_with_two_posts"]
    user2 = test_users_with_posts_reactions["user_with_one_post"]

    # user1 reacted on user2's post
    post = user2.posts[0]

    result = reaction_service._get_reaction(
        current_user_id=user1.id,
        post_id=post.id,
    )

    assert result.user_id == user1.id
    assert result.type == ReactionType.like


def test_get_reaction_for_a_post_not_found(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user1 = test_users_with_posts_reactions["user_with_two_posts"]

    # User1 did not react to their own first post
    post = user1.posts[0]

    with pytest.raises(ReactionNotFound):
        reaction_service._get_reaction(
            current_user_id=user1.id,
            post_id=post.id,
        )


# -----------------------------
# Create post reaction tests
# -----------------------------


def test_create_reaction(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user = test_users_with_posts_reactions["user_with_two_posts"]

    reaction = reaction_service.add_post_reaction(
        current_user_id=user.id,
        post_id=user.posts[0].id,
        reaction=ReactionCreate(type=ReactionType.like),
    )

    assert reaction.type == ReactionType.like
    assert reaction.user_id == user.id


def test_create_reaction_already_exists(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user = test_users_with_posts_reactions["user_with_two_posts"]
    post_id = test_users_with_posts_reactions["user_with_one_post"].posts[0].id
    with pytest.raises(ReactionAlreadyExists):
        reaction_service.add_post_reaction(
            current_user_id=user.id,
            post_id=post_id,
            reaction=ReactionCreate(type=ReactionType.like),
        )


# -----------------------------
# Get post reactions tests
# -----------------------------


def test_get_post_reactions(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user = test_users_with_posts_reactions["user_with_two_posts"]

    reactions = reaction_service.get_post_reactions(
        current_user_id=user.id,
        post_id=user.posts[0].id,
    )

    assert len(reactions) == 2


# -----------------------------
# Update post reaction tests
# -----------------------------


def test_update_reaction_success(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user = test_users_with_posts_reactions["user_with_two_posts"]

    updated_reaction = reaction_service.update_post_reaction(
        current_user_id=user.id,
        post_id=user.posts[1].id,  # User1 reacted on user1's post
        reaction_update=ReactionEdit(type=ReactionType.fire),
    )

    assert updated_reaction.type == ReactionType.fire


# -----------------------------
# Delete post reaction tests
# -----------------------------


def test_delete_reaction_success(
    reaction_service: ReactionService, test_users_with_posts_reactions
):
    user = test_users_with_posts_reactions["user_with_two_posts"]

    reaction = reaction_service.delete_post_reaction(
        current_user_id=user.id,
        post_id=user.posts[1].id,  # User1 reacted on user1's post
    )

    assert reaction is None
