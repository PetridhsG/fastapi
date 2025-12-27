from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions.user import UserNotAllowedToViewResource, UserNotFound
from app.core.security.jwt import verify_access_token
from app.db.database import get_db
from app.db.models import User
from app.services.helpers.user_queries import UserHelper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get the current user from the access token."""
    token_data = verify_access_token(token)
    user = db.get(User, token_data.user_id)
    if not user:
        raise UserNotFound
    return user


def can_view_target_user(
    username: str = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if the current user can view the target user."""
    helper = UserHelper(db)
    target_user = helper.get_target_user(username)
    if not helper.can_view_user(current_user.id, target_user):
        raise UserNotAllowedToViewResource

    return target_user
