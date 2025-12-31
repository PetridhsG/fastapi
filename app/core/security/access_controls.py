from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions.auth import AuthUserCannotBeAuthenticated
from app.core.exceptions.user import UserNotAllowedToViewResource, UserNotFound
from app.core.security.jwt import verify_access_token
from app.db.database import get_db
from app.db.models import User
from app.db.models.follow import Follow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get the current user from the access token."""
    token_data = verify_access_token(token)
    user = db.get(User, token_data.user_id)
    if not user:
        raise AuthUserCannotBeAuthenticated()
    return user


def can_view_target_user(
    username: str = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Return the target user if the current user is allowed to view them.

    Raises:
        UserNotAllowedToViewResource: If current user cannot view target user.
    """
    # Get target user
    target_user = db.query(User).filter(User.username == username).first()
    if not target_user:
        raise UserNotFound()

    # Check visibility
    if not target_user.is_private:
        return target_user
    if target_user.id == current_user.id:
        return target_user

    # Check if current user follows target user and is accepted
    follow_exists = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.followee_id == target_user.id,
            Follow.accepted.is_(True),
        )
        .first()
    )
    if not follow_exists:
        raise UserNotAllowedToViewResource()

    return target_user
