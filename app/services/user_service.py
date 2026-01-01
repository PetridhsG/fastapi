from typing import List, Optional

from sqlalchemy import case, func
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
from app.services.helpers.subqueries.user_subqueries import UserSubqueries
from app.services.helpers.user_helper import UserHelper


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_helper = UserHelper(db)

    def create_user(self, user_create: UserCreate) -> UserCreatedOut:
        """Create a new user and hash password; raises UserEmailAlreadyExists on duplicate email."""
        if self.db.query(User).filter(User.email == user_create.email).first():
            raise UserEmailAlreadyExists()

        if self.db.query(User).filter(User.username == user_create.username).first():
            raise UsernameAlreadyExists()

        hashed_password = hash_password(user_create.password)
        user_data = user_create.model_dump()
        user_data["hashed_password"] = hashed_password
        user_data.pop("password")

        new_user = User(**user_data)
        self.db.add(new_user)

        self.db.flush()
        self.db.refresh(new_user)

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
        """Search users by username with pagination."""
        return self._query_users(
            current_user_id=current_user_id, search=query, limit=limit
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
        """Get followers of the target user."""
        return self._query_users(
            current_user_id=current_user_id,
            search=search,
            join_model=Follow,
            join_condition=User.id == Follow.follower_id,
            join_filters=[
                Follow.followee_id == target_user_id,
                Follow.accepted.is_(True),
            ],
            limit=limit,
            offset=offset,
        )

    def get_user_following(
        self,
        current_user_id: int,
        target_user_id: int,
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = "",
    ) -> List[UserListItemOut]:
        """Get users that the target user is following."""
        return self._query_users(
            current_user_id=current_user_id,
            search=search,
            join_model=Follow,
            join_condition=User.id == Follow.followee_id,
            join_filters=[
                Follow.follower_id == target_user_id,
                Follow.accepted.is_(True),
            ],
            limit=limit,
            offset=offset,
        )

    def update_user(self, user_id: int, data: UserEdit) -> User:
        """Update user information; raises UserNotFound or UsernameAlreadyExists."""

        user = self.user_helper.get_user_by_id(user_id)

        if data.username and data.username != user.username:
            if self.db.query(User).filter(User.username == data.username).first():
                raise UsernameAlreadyExists()
            user.username = data.username

        if data.bio is not None:
            user.bio = data.bio

        if data.is_private is not None:
            user.is_private = data.is_private

        self.db.flush()
        return user

    def change_password(self, user_id: int, data: UserChangePassword) -> None:
        """Change user's password; raises UserNotFound or InvalidPassword."""
        user = self.user_helper.get_user_by_id(user_id)

        if not verify_password(data.current_password, user.hashed_password):
            raise UserInvalidPassword()

        if verify_password(data.new_password, user.hashed_password):
            raise UserPasswordUnchanged()

        user.hashed_password = hash_password(data.new_password)
        self.db.flush()

    def delete_user(self, user_id: int) -> None:
        """Delete user"""
        user = self.user_helper.get_user_by_id(user_id)
        self.db.delete(user)
        self.db.flush()

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
            raise UserNotFound()

        # Hide is_following for current user
        user_dict = dict(user._mapping)
        if user_dict["id"] == current_user_id:
            user_dict["is_following"] = None

        return UserPublicOut(**user_dict)

    def _query_users(
        self,
        current_user_id: int,
        search: Optional[str] = "",
        join_model=None,
        join_condition=None,
        join_filters=None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[UserListItemOut]:
        """
        Centralized user query logic.
        - join_model: SQLAlchemy model to join (e.g., Follow)
        - join_condition: the ON condition for join
        - join_filters: additional filters after join
        """
        q = (search or "").strip().lower()

        query = self.db.query(
            User.id,
            User.username,
            UserSubqueries.followers_count_subq(self.db).label("followers_count"),
            UserSubqueries.is_following_subq(self.db, current_user_id).label(
                "is_following"
            ),
        )

        if join_model:
            query = query.join(join_model, join_condition)
        if join_filters:
            query = query.filter(*join_filters)

        if q:
            query = query.filter(User.username.ilike(f"%{q}%"))

        query = query.order_by(
            case(
                (func.lower(User.username) == q, 0),
                (func.lower(User.username).like(f"{q}%"), 1),
                else_=2,
            ),
            User.username.asc(),
        )

        return query.limit(limit).offset(offset).all()
