from sqlalchemy.orm import Session

from app.core.exceptions.user import UserNotFound
from app.db.models.follow import Follow
from app.db.models.user import User


class UserHelper:

    def __init__(self, db: Session):
        self.db = db

    def can_view_user(self, current_user_id: int, target_user: User) -> bool:
        """Return True if current user can view target_user."""
        if not target_user.is_private:
            return True
        if target_user.id == current_user_id:
            return True

        return (
            self.db.query(Follow)
            .filter(
                Follow.follower_id == current_user_id,
                Follow.followee_id == target_user.id,
                Follow.accepted.is_(True),
            )
            .first()
            is not None
        )

    def get_user_by_id(self, user_id: int) -> User:
        """Internal helper to fetch user by ID."""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFound
        return user

    def get_target_user(self, username: str) -> User:
        """Fetch a user by username; raises UserNotFound if missing."""
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise UserNotFound
        return user
