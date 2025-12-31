from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.comment import Comment
from app.db.models.reaction import Reaction


class PostSubqueries:

    @staticmethod
    def comments_count_subq(db: Session):
        """Return a correlated subquery for comments count per post."""
        return (
            db.query(
                Comment.post_id,
                func.count(Comment.id).label("comments_count"),
            )
            .group_by(Comment.post_id)
            .subquery()
        )

    @staticmethod
    def reactions_count_subq(db: Session):
        """Return a correlated subquery for reactions count per post."""
        return (
            db.query(
                Reaction.post_id,
                func.count(Reaction.user_id).label("reactions_count"),
            )
            .group_by(Reaction.post_id)
            .subquery()
        )

    @staticmethod
    def user_reaction_subq(db: Session, current_user_id: int):
        """Return a correlated subquery to check if current user reacted to this post."""
        return (
            db.query(
                Reaction.post_id,
                Reaction.type.label("user_reacted"),
            )
            .filter(Reaction.user_id == current_user_id)
            .subquery()
        )
