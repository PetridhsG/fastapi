from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions.auth import AuthUserCannotBeAuthenticated
from app.core.exceptions.post import PostNotFound
from app.core.exceptions.user import UserNotAllowedToViewResource, UserNotFound
from app.core.security.jwt import verify_access_token
from app.db.database import get_db
from app.db.models import User
from app.db.models.follow import Follow
from app.db.models.post import Post

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
) -> int:
    """
    Raise if current_user cannot view target user.
    Return target user_id if allowed.
    """
    # Get target user
    target_user = db.query(User).filter(User.username == username).first()
    if not target_user:
        raise UserNotFound()

    # Public user or self
    if not target_user.is_private or target_user.id == current_user.id:
        return target_user.id

    # Check if current user follows target user
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

    return target_user.id


def can_view_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> int:
    """
    Raises an exception if current_user cannot view the post.
    Returns the post_id if allowed.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise PostNotFound()

    owner = db.query(User).filter(User.id == post.owner_id).first()
    if not owner:
        raise UserNotFound()

    if owner.is_private and owner.id != current_user.id:
        # check if current user follows owner
        follow_exists = (
            db.query(Follow)
            .filter(
                Follow.follower_id == current_user.id,
                Follow.followee_id == owner.id,
                Follow.accepted.is_(True),
            )
            .first()
        )
        if not follow_exists:
            raise UserNotAllowedToViewResource()

    return post_id
