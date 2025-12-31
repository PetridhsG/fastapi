from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.follow_service import FollowService
from app.services.post_service import PostService
from app.services.reaction_service import ReactionService
from app.services.user_service import UserService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(db)


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db)


def get_reaction_service(db: Session = Depends(get_db)) -> ReactionService:
    return ReactionService(db)


def get_follow_service(db: Session = Depends(get_db)) -> FollowService:
    return FollowService(db)
