from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.schemas.post import (
    PostCreate,
    PostCreatedOut,
    PostEdit,
    PostListItemOut,
    PostOut,
)
from app.api.v1.schemas.user import UserListItemOut
from app.core.exceptions.post import PostNotFound, PostUserNotAllowed
from app.core.exceptions.user import UserNotFound
from app.db.models.post import Post
from app.db.models.reaction import Reaction
from app.db.models.user import User
from app.services.helpers.subqueries.post_subqueries import PostSubqueries
from app.services.helpers.subqueries.user_subqueries import UserSubqueries
from app.services.helpers.user_helper import UserHelper


class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.user_helper = UserHelper(db)

    def create_post(
        self, current_user_id: int, post_create: PostCreate
    ) -> PostCreatedOut:
        """Create a new post and return it."""
        new_post = Post(**post_create.model_dump(), owner_id=current_user_id)
        self.db.add(new_post)
        self.db.flush()
        self.db.refresh(new_post)
        return new_post

    def get_user_posts(
        self,
        current_user_id: int,
        target_user_id: int,
        limit: int,
        offset: int,
    ) -> List[PostListItemOut]:
        """Get posts for a given user with pagination."""

        return (
            self._build_post_base_query(current_user_id)
            .filter(Post.owner_id == target_user_id)
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()

    def get_post(self, current_user_id: int, post_id: int) -> PostOut:
        """Get a post by ID; raises PostNotFound if not found."""

        query = self._build_post_base_query(current_user_id).filter(Post.id == post_id)

        post_row = query.first()
        if not post_row:
            raise PostNotFound()

        # Owner info using subqueries
        owner_row = (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .filter(User.id == post_row.owner_id)
            .first()
        )

        if not owner_row:
            raise UserNotFound()

        owner_out = UserListItemOut(
            id=owner_row.id,
            username=owner_row.username,
            is_following=owner_row.is_following,
            followers_count=owner_row.followers_count,
        )

        # Reactions grouped by type
        reactions_by_type_rows = (
            self.db.query(Reaction.type, func.count(Reaction.user_id).label("count"))
            .filter(Reaction.post_id == post_id)
            .group_by(Reaction.type)
            .all()
        )
        reactions_by_type = {r.type.value: r.count for r in reactions_by_type_rows}

        # Build PostOut
        post_out = PostOut(
            id=post_row.id,
            title=post_row.title,
            content=post_row.content,
            owner_id=post_row.owner_id,
            created_at=post_row.created_at,
            comments_count=post_row.comments_count,
            reactions_count=post_row.reactions_count,
            user_reacted=post_row.user_reacted,
            owner=owner_out,
            reactions_by_type=reactions_by_type,
        )

        return post_out

    def update_post(
        self,
        current_user_id: int,
        post_id: int,
        post_update: PostEdit,
    ) -> PostCreatedOut:
        """Update a post."""

        post = self._get_post_for_user(current_user_id, post_id)

        if post_update.title is not None:
            post.title = post_update.title
        if post_update.content is not None:
            post.content = post_update.content

        self.db.flush()
        self.db.refresh(post)
        return post

    def delete_post(self, current_user_id: int, post_id: int) -> None:
        """Delete a post."""

        post = self._get_post_for_user(current_user_id, post_id)

        self.db.delete(post)
        self.db.flush()

    def _build_post_base_query(self, current_user_id: int):
        comments_count_sq = PostSubqueries.comments_count_subq(self.db)
        reactions_count_sq = PostSubqueries.reactions_count_subq(self.db)
        user_reaction_sq = PostSubqueries.user_reaction_subq(self.db, current_user_id)

        query = (
            self.db.query(
                Post.id,
                Post.title,
                Post.content,
                Post.owner_id,
                Post.created_at,
                func.coalesce(comments_count_sq.c.comments_count, 0).label(
                    "comments_count"
                ),
                func.coalesce(reactions_count_sq.c.reactions_count, 0).label(
                    "reactions_count"
                ),
                user_reaction_sq.c.user_reacted,
            )
            .outerjoin(comments_count_sq, comments_count_sq.c.post_id == Post.id)
            .outerjoin(reactions_count_sq, reactions_count_sq.c.post_id == Post.id)
            .outerjoin(user_reaction_sq, user_reaction_sq.c.post_id == Post.id)
        )

        return query

    def _get_post_for_user(self, current_user_id: int, post_id: int) -> Post:
        """Fetch a post and ensure the current user is allowed to modify it."""
        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise PostNotFound()

        if post.owner_id != current_user_id:
            raise PostUserNotAllowed()

        return post
