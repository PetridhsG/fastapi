from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.api.v1.schemas.user import UserCreate, UserSearchOut
from app.core.exceptions.user import (
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.core.security.password import hash_password
from app.db.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
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

    def search_users(self, current_user_id: int, query: str) -> List[UserSearchOut]:
        """
        Search users by username and return minimal info + follow info.
        """
        users = (
            self.db.query(User)
            .options(joinedload(User.followers))
            .filter(User.username.ilike(f"%{query}%"))
            .all()
        )

        results: List[UserSearchOut] = []

        for user in users:
            is_following = any(
                f.follower_id == current_user_id and f.accepted for f in user.followers
            )
            followers_count = sum(f.accepted for f in user.followers)

            results.append(
                UserSearchOut(
                    id=user.id,
                    username=user.username,
                    is_following=is_following,
                    followers_count=followers_count,
                )
            )

        return results
