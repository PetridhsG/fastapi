from typing import List, Optional

from sqlalchemy import case, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing_extensions import Literal

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
    InvalidPassword,
    PasswordUnchanged,
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotAllowed,
    UserNotFound,
)
from app.core.security.password import hash_password, verify_password
from app.db.models import User
from app.db.models.follow import Follow
from app.services.helpers.user_subqueries import UserSubqueries


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> UserCreatedOut:
        """Create a new user and hash password; raises UserAlreadyExists on duplicate email."""
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
            raise UserAlreadyExists

        return new_user

    def get_current_user(self, user_id: int) -> UserPublicOut | None:
        """Get current user; raises UserNotFound if not found."""
        return self._get_user_by_id(user_id)

    def get_current_user_settings(self, user_id: int) -> UserSettingsOut | None:
        """Get current user; raises UserNotFound if not found."""
        return self._get_user_by_id(user_id)

    def search_users(
        self, current_user_id: int, query: str, limit: int = 10
    ) -> List[UserListItemOut]:
        """Search users by username."""
        q = query.strip().lower()

        users = (
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

        return [user for user in users]

    def get_user_by_username(
        self, current_user_id: int, username: str
    ) -> UserPublicOut | None:
        """Get public user information by username; raises UserNotFound if not found."""
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

        # If the user is viewing their own profile, set is_following to None
        user_dict = dict(user._mapping)
        if user_dict["id"] == current_user_id:
            user_dict["is_following"] = None

        return UserPublicOut(**user_dict)

    def get_user_followers(
        self, current_user_id: int, username: str, **kwargs
    ) -> List[UserListItemOut]:
        """Get followers of a user; raises UserNotFound if not found."""
        return self._get_user_follow_relationship(
            current_user_id, username, relationship="followers", **kwargs
        )

    def get_user_following(
        self, current_user_id: int, username: str, **kwargs
    ) -> List[UserListItemOut]:
        """Get following of a user; raises UserNotFound if not found."""
        return self._get_user_follow_relationship(
            current_user_id, username, relationship="following", **kwargs
        )

    def update_user(self, user_id: int, data: UserEdit) -> User:
        """Update user information; raises UserNotFound or UsernameAlreadyExists."""

        user = self._get_user_by_id(user_id)

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
        user = self._get_user_by_id(user_id)

        # Verify current password
        if not verify_password(data.current_password, user.hashed_password):
            raise InvalidPassword

        # Prevent reusing the same password
        if verify_password(data.new_password, user.hashed_password):
            raise PasswordUnchanged

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

    def _get_user_by_id(self, user_id: int) -> User:
        """Internal helper to fetch user by ID."""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFound
        return user

    def _get_user_follow_relationship(
        self,
        current_user_id: int,
        target_username: str,
        relationship: Literal["followers", "following"],
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = "",
    ) -> List[UserListItemOut]:
        """Internal helper to fetch followers or following of a user with access control."""
        q = (search or "").strip().lower()

        # Use the shared access control helper
        target_user = self._get_target_user_with_access(
            current_user_id, target_username
        )

        # Determine join/filter columns based on relationship type
        if relationship == "followers":
            join_condition = User.id == Follow.follower_id
            filter_condition = Follow.followee_id == target_user.id
        elif relationship == "following":
            join_condition = User.id == Follow.followee_id
            filter_condition = Follow.follower_id == target_user.id

        rows = (
            self.db.query(
                User.id,
                User.username,
                UserSubqueries.followers_count_subq(self.db).label("followers_count"),
                UserSubqueries.is_following_subq(self.db, current_user_id).label(
                    "is_following"
                ),
            )
            .select_from(User)
            .join(Follow, join_condition)
            .filter(filter_condition, Follow.accepted.is_(True))
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

        return [row for row in rows]

    def _get_target_user_with_access(
        self,
        current_user_id: int,
        username: str,
    ) -> User:
        """
        Retrieve a target user by username and enforce access control.

        Access rules:
        - The current user can always access their own data.
        - Public users are accessible to anyone.
        - Private users are accessible only if the current user follows them.

        Raises:
            UserNotFound: if the user does not exist.
            UserNotAllowed: if the current user is not allowed to access a private user.
        """
        target_user = self.db.query(User).filter(User.username == username).first()
        if not target_user:
            raise UserNotFound

        # Access control for private accounts
        if target_user.id != current_user_id and target_user.is_private:
            is_following = (
                self.db.query(Follow)
                .filter(
                    Follow.follower_id == current_user_id,
                    Follow.followee_id == target_user.id,
                    Follow.accepted.is_(True),
                )
                .first()
            )
            if not is_following:
                raise UserNotAllowed

        return target_user
