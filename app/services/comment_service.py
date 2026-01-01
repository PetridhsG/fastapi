from typing import List

from sqlalchemy.orm import Session

from app.api.v1.schemas.comment import (
    CommentCreate,
    CommentCreatedOut,
    CommentEdit,
    CommentOut,
)
from app.core.exceptions.comment import CommentNotFound, CommentUserNotAllowed
from app.db.models.comment import Comment
from app.services.helpers.user_helper import UserHelper


class CommentService:
    def __init__(self, db: Session):
        self.user_helper = UserHelper(db)
        self.db = db

    def add_post_comment(
        self, current_user_id: int, post_id: int, comment_create: CommentCreate
    ) -> CommentOut:
        """Create a new comment on a post and return it."""
        new_comment = Comment(
            **comment_create.model_dump(), owner_id=current_user_id, post_id=post_id
        )
        self.db.add(new_comment)
        self.db.flush()
        self.db.refresh(new_comment)
        return new_comment

    def get_post_comments(
        self,
        current_user_id: int,
        post_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> List[CommentOut]:
        """Get comments for a given post with minimal owner info and pagination."""

        comments = (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        result: List[CommentOut] = []
        for comment in comments:
            owner_out = self.user_helper.get_user_list_item_out(
                user_id=comment.owner_id,
                current_user_id=current_user_id,
            )

            result.append(
                CommentOut(
                    id=comment.id,
                    content=comment.content,
                    created_at=comment.created_at,
                    post_id=comment.post_id,
                    owner=owner_out,
                )
            )

        return result

    def update_post_comment(
        self,
        current_user_id: int,
        post_id: int,
        comment_id: int,
        comment_update: CommentEdit,
    ) -> CommentCreatedOut:
        """Update a comment on a post and return minimal info."""

        comment = self._get_comment(current_user_id, post_id, comment_id)

        if comment_update.content is not None:
            comment.content = comment_update.content

        self.db.flush()
        self.db.refresh(comment)

        return comment

    def delete_post_comment(
        self,
        current_user_id: int,
        post_id: int,
        comment_id: int,
    ) -> None:
        """Delete a comment on a post."""

        comment = self._get_comment(current_user_id, post_id, comment_id)

        self.db.delete(comment)
        self.db.flush()

    def _get_comment(
        self, current_user_id: int, post_id: int, comment_id: int
    ) -> Comment:
        """
        Fetch a comment by ID and post ID, and ensure the current user is the owner.\
        Raises:
            CommentNotFound
            CommentUserNotAllowed
        """
        comment = (
            self.db.query(Comment)
            .filter(Comment.id == comment_id, Comment.post_id == post_id)
            .first()
        )
        
        if not comment:
            raise CommentNotFound()

        if comment.owner_id != current_user_id:
            raise CommentUserNotAllowed()

        return comment
