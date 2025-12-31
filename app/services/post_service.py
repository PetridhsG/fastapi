from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.schemas.post import PostCreate, PostCreatedOut, PostListItemOut
from app.db.models.post import Post
from app.services.helpers.subqueries.post_subqueries import PostSubqueries
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

    def get_posts_by_username(
        self,
        current_user_id: int,
        target_user_id: int,
        limit: int,
        offset: int,
    ) -> List[PostListItemOut]:
        """Get posts by username; raises UserNotFound if not found."""

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
            .outerjoin(
                comments_count_sq,
                comments_count_sq.c.post_id == Post.id,
            )
            .outerjoin(
                reactions_count_sq,
                reactions_count_sq.c.post_id == Post.id,
            )
            .outerjoin(
                user_reaction_sq,
                user_reaction_sq.c.post_id == Post.id,
            )
            .filter(Post.owner_id == target_user_id)
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return query.all()
