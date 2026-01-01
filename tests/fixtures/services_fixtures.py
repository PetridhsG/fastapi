import pytest
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.follow_service import FollowService
from app.services.post_service import PostService
from app.services.reaction_service import ReactionService
from app.services.user_service import UserService


@pytest.fixture
def auth_service(session: Session) -> AuthService:
    """Provides an AuthService instance with a fresh test session."""
    return AuthService(session)


@pytest.fixture
def user_service(session: Session) -> UserService:
    """Provides an UserService instance with a fresh test session."""
    return UserService(session)


@pytest.fixture
def post_service(session: Session) -> PostService:
    """Provides a PostService instance with a fresh test session."""
    return PostService(session)


@pytest.fixture
def comment_service(session: Session) -> CommentService:
    """Provides a CommentService instance with a fresh test session."""
    return CommentService(session)


@pytest.fixture
def reaction_service(session: Session) -> ReactionService:
    """Provides a ReactionService instance with a fresh test session."""
    return ReactionService(session)


@pytest.fixture
def follow_service(session: Session) -> FollowService:
    """Provides a FollowService instance with a fresh test session."""
    return FollowService(session)
