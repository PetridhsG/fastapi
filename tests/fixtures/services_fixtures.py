import pytest
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserCreate
from app.core.security.password import hash_password
from app.db.models.follow import Follow
from app.db.models.post import Post
from app.db.models.user import User
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


@pytest.fixture(scope="function")
def test_users(session: Session):
    """Creates three test users directly using the session."""
    users_data = [
        {
            "username": "exampleUser1",
            "email": "user1@example.com",
            "password": "User1Pass!",
            "bio": "",
            "is_private": False,
        },
        {
            "username": "exampleUser2",
            "email": "user2@example.com",
            "password": "User2Pass!",
            "bio": "This is user 2's bio.",
            "is_private": True,
        },
    ]

    users = []
    for u in users_data:
        user = User(
            username=u["username"],
            email=u["email"],
            hashed_password=hash_password(u["password"]),
            bio=u["bio"],
            is_private=u["is_private"],
        )
        session.add(user)
        users.append(user)

    session.commit()
    return users


@pytest.fixture(scope="function")
def test_users_with_follow(user_service: UserService, session: Session):
    """
    Creates users with different followers/following scenarios:
    - user1: follows user2 and user3
    - user2: follows user3, has user1 as follower
    - user3: follows no one, has user1 and user3 as followers
    - user4: follows no one, has no followers
    """

    users_data = [
        UserCreate(username="user1", email="user1@email.com", password="User1Pass!"),
        UserCreate(username="user2", email="user2@email.com", password="User2Pass!"),
        UserCreate(username="user3", email="user3@email.com", password="User3Pass!"),
        UserCreate(
            username="user4",
            email="user4@email.com",
            password="User4Pass!",
            is_private=True,
        ),
    ]
    users = [user_service.create_user(u) for u in users_data]

    session.add_all(
        [
            Follow(follower_id=users[0].id, followee_id=users[1].id, accepted=True),
            Follow(follower_id=users[0].id, followee_id=users[2].id, accepted=True),
            Follow(follower_id=users[1].id, followee_id=users[2].id, accepted=True),
        ]
    )

    session.commit()

    return {
        "user1": users[0],
        "user2": users[1],
        "user3": users[2],
        "user4": users[3],
    }


@pytest.fixture(scope="function")
def user_with_posts(user_service: UserService, session):
    user_data = UserCreate(
        username="postuser", email="postuser@example.com", password="Pass123!"
    )
    user = user_service.create_user(user_data)

    posts = [
        Post(title="Post 1", content="Content 1", owner_id=user.id),
        Post(title="Post 2", content="Content 2", owner_id=user.id),
    ]
    session.add_all(posts)
    session.commit()

    return user
