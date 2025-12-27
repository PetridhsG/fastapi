from typing import List, Optional

from sqlalchemy import case, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import (
    UserChangePassword,
    UserCreate,
    UserCreatedOut,
    UserEdit,
    UserListItemOut,
    UserPublicOut,
    UserSettingsOut,
)
from app.core.exceptions.user import (
    UserEmailAlreadyExists,
    UserInvalidPassword,
    UsernameAlreadyExists,
    UserNotFound,
    UserPasswordUnchanged,
)
from app.core.security.password import hash_password, verify_password
from app.db.models import User
from app.db.models.follow import Follow
from app.services.helpers.user_queries import UserHelper
from app.services.helpers.user_subqueries import UserSubqueries


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_helper = UserHelper(db)

    def create_user(self, user_create: UserCreate) -> UserCreatedOut:
        """Create a new user and hash password; raises UserEmailAlreadyExists on duplicate email."""
        if self.db.query(User).filter(User.email == user_create.email).first():
            raise UserEmailAlreadyExists

        if self.db.query(User).filter(User.username == user_create.username).first():
            raise UsernameAlreadyExists

        hashed_password = hash_password(user_create.password)
        user_data = user_create.model_dump()
        user_data["hashed_password"] = hashed_password
        user_data.pop("password")

        new_user = User(**user_data)
        self.db.add(new_user)

        try:
            self.db.commit()
            self.db.refresh(new_user)
        except IntegrityError:
            # Safety net for race conditions
            self.db.rollback()

        return new_user

    def get_current_user(self, user_id: int) -> UserPublicOut:
        """Get current user."""
        user = self.user_helper.get_user_by_id(user_id)
        return self._get_public_user(current_user_id=user_id, username=user.username)

    def get_current_user_settings(self, user_id: int) -> UserSettingsOut | None:
        """Get current user settings; raises UserNotFound if not found."""
        return self.user_helper.get_user_by_id(user_id)

    def search_users(
        self, current_user_id: int, query: str, limit: int = 10
    ) -> List[UserListItemOut]:
        """Search users by username."""
        q = query.strip().lower()

        return (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .filter(User.username.ilike(f"%{q}%"))
            .order_by(
                case(
                    (func.lower(User.username) == q, 0),
                    (func.lower(User.username).like(f"{q}%"), 1),
                    else_=2,
                ),
                User.username.asc(),
            )
            .limit(limit)
            .all()
        )

    def get_user_by_username(
        self, current_user_id: int, username: str
    ) -> UserPublicOut:
        """Get user by username; raises UserNotFound if not found."""
        return self._get_public_user(current_user_id=current_user_id, username=username)

    def get_user_followers(
        self,
        current_user_id: int,
        target_user_id: int,
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = "",
    ) -> List[UserListItemOut]:
        """Get followers of a user; raises UserNotFound if not found."""
        q = (search or "").strip().lower()

        return (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .select_from(User)
            .join(Follow, User.id == Follow.follower_id)
            .filter(Follow.followee_id == target_user_id, Follow.accepted.is_(True))
            .filter(User.username.ilike(f"%{q}%"))
            .order_by(
                case(
                    (func.lower(User.username) == q, 0),
                    (func.lower(User.username).like(f"{q}%"), 1),
                    else_=2,
                ),
                User.username.asc(),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_user_following(
        self,
        current_user_id: int,
        target_user_id: int,
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = "",
    ) -> List[UserListItemOut]:
        """Get following of a user; assumes access already checked."""
        q = (search or "").strip().lower()

        return (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .select_from(User)
            .join(Follow, User.id == Follow.followee_id)
            .filter(Follow.follower_id == target_user_id, Follow.accepted.is_(True))
            .filter(User.username.ilike(f"%{q}%"))
            .order_by(
                case(
                    (func.lower(User.username) == q, 0),
                    (func.lower(User.username).like(f"{q}%"), 1),
                    else_=2,
                ),
                User.username.asc(),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )

    def update_user(self, user_id: int, data: UserEdit) -> User:
        """Update user information; raises UserNotFound or UsernameAlreadyExists."""

        user = self.user_helper.get_user_by_id(user_id)

        if data.username and data.username != user.username:
            if self.db.query(User).filter(User.username == data.username).first():
                raise UsernameAlreadyExists
            user.username = data.username

        if data.bio is not None:
            user.bio = data.bio

        if data.is_private is not None:
            user.is_private = data.is_private

        self.db.commit()
        self.db.refresh(user)
        return user

    def change_password(self, user_id: int, data: UserChangePassword) -> None:
        """Change user's password; raises UserNotFound or InvalidPassword."""
        user = self.user_helper.get_user_by_id(user_id)

        # Verify current password
        if not verify_password(data.current_password, user.hashed_password):
            raise UserInvalidPassword

        # Prevent reusing the same password
        if verify_password(data.new_password, user.hashed_password):
            raise UserPasswordUnchanged

        # Hash and update new password
        user.hashed_password = hash_password(data.new_password)
        self.db.commit()
        self.db.refresh(user)

    def delete_user(self, user_id: int) -> None:
        """Delete user; raises UserNotFound."""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFound

        self.db.delete(user)
        self.db.commit()

    def _get_public_user(
        self,
        current_user_id: int,
        username: str,
    ) -> UserPublicOut:
        """Get public user info by user_id or username."""
        user = (
            self.db.query(
                User.id,
                User.username,
                User.bio,
                User.is_private,
                UserSubqueries.posts_count_subq(self.db).label("posts_count"),
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.following_count_subq(self.db).label("following_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .filter(User.username == username)
            .first()
        )

        if not user:
            raise UserNotFound

        # Hide is_following for current user
        user_dict = dict(user._mapping)
        if user_dict["id"] == current_user_id:
            user_dict["is_following"] = None

        return UserPublicOut(**user_dict)
