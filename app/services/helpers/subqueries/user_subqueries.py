from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.follow import Follow
from app.db.models.post import Post
from app.db.models.user import User


class UserSubqueries:

    @staticmethod
    def posts_count_subq(db: Session):
        """Return a correlated subquery for posts count per user."""
        return (
            db.query(func.count(Post.id))
            .filter(Post.owner_id == User.id)
            .correlate(User)
            .scalar_subquery()
        )

    @staticmethod
    def followers_count_subq(db: Session):
        """Return a correlated subquery for followers count per user."""
        return (
            db.query(func.count(Follow.follower_id))
            .filter(
                Follow.followee_id == User.id,
                Follow.accepted.is_(True),
            )
            .correlate(User)
            .scalar_subquery()
        )

    @staticmethod
    def following_count_subq(db: Session):
        """Return a correlated subquery for following count per user."""
        return (
            db.query(func.count(Follow.followee_id))
            .filter(
                Follow.follower_id == User.id,
                Follow.accepted.is_(True),
            )
            .correlate(User)
            .scalar_subquery()
        )

    @staticmethod
    def is_following_subq(db: Session, current_user_id: int):
        """Return a correlated subquery to check if current user follows this user."""
        return (
            db.query(Follow)
            .filter(
                Follow.follower_id == current_user_id,
                Follow.followee_id == User.id,
                Follow.accepted.is_(True),
            )
            .correlate(User)
            .exists()
        )
