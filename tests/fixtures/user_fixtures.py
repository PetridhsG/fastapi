import pytest
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserCreate
from app.core.security.password import hash_password
from app.db.models.follow import Follow
from app.db.models.post import Post
from app.db.models.user import User
from app.services.user_service import UserService


@pytest.fixture(scope="function")
def test_users(session: Session):
    users_data = [
        {
            "username": "exampleuser1",
            "email": "user1@example.com",
            "password": "User1Pass!",
            "is_private": False,
        },
        {
            "username": "exampleuser2",
            "email": "user2@example.com",
            "password": "User2Pass!",
            "is_private": True,
        },
    ]

    users = []
    for u in users_data:
        user = User(
            username=u["username"],
            email=u["email"],
            hashed_password=hash_password(u["password"]),
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
    - user4: follows no one, has no followers and no follow requests
    - user5: sent follow request to user1 and user6 (not accepted)
    - user6: have follow request from user5 (not accepted)
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
        UserCreate(username="user5", email="user5@email.com", password="User5Pass!"),
        UserCreate(username="user6", email="user6@email.com", password="User6Pass!"),
    ]
    users = [user_service.create_user(u) for u in users_data]

    session.add_all(
        [
            Follow(follower_id=users[0].id, followee_id=users[1].id, accepted=True),
            Follow(follower_id=users[0].id, followee_id=users[2].id, accepted=True),
            Follow(follower_id=users[1].id, followee_id=users[2].id, accepted=True),
            Follow(follower_id=users[4].id, followee_id=users[0].id, accepted=False),
            Follow(follower_id=users[4].id, followee_id=users[5].id, accepted=False),
        ]
    )

    session.commit()

    return {
        "user1": users[0],
        "user2": users[1],
        "user3": users[2],
        "user4": users[3],
        "user5": users[4],
        "user6": users[5],
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
