from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserListItemOut
from app.core.exceptions.user import UserNotFound
from app.db.models.user import User
from app.services.helpers.subqueries.user_subqueries import UserSubqueries


class UserHelper:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        """Internal helper to fetch user by ID."""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFound()
        return user

    def get_target_user(self, username: str) -> User:
        """Fetch a user by username; raises UserNotFound if missing."""
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise UserNotFound()
        return user

    def get_user_list_item_out(
        self, user_id: int, current_user_id: int
    ) -> UserListItemOut:
        """Fetch minimal user info for lists (followers, owner in posts/comments)."""
        owner_row = (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .filter(User.id == user_id)
            .first()
        )

        if not owner_row:
            raise UserNotFound()

        return UserListItemOut(
            id=owner_row.id,
            username=owner_row.username,
            is_following=owner_row.is_following,
            followers_count=owner_row.followers_count,
        )
