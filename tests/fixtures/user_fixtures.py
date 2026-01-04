import pytest
from sqlalchemy.orm import Session

from app.core.security.password import hash_password
from app.db.models.follow import Follow
from app.db.models.post import Post
from app.db.models.user import User


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
def test_users_with_follow(session: Session):
    """
    Creates users with different followers/following scenarios:

    - user1: follows user2 and user3
    - user2: follows user3, has user1 as follower
    - user3: follows no one, has user1 and user2 as followers
    - user4: follows no one, has no followers and no follow requests
    - user5: sent follow request to user1 and user6 (not accepted)
    - user6: has follow request from user5 (not accepted)
    """

    users = [
        User(
            username="user1",
            email="user1@email.com",
            hashed_password=hash_password("User1Pass!"),
            is_private=False,
        ),
        User(
            username="user2",
            email="user2@email.com",
            hashed_password=hash_password("User2Pass!"),
            is_private=False,
        ),
        User(
            username="user3",
            email="user3@email.com",
            hashed_password=hash_password("User3Pass!"),
            is_private=False,
        ),
        User(
            username="user4",
            email="user4@email.com",
            hashed_password=hash_password("User4Pass!"),
            is_private=True,
        ),
        User(
            username="user5",
            email="user5@email.com",
            hashed_password=hash_password("User5Pass!"),
            is_private=False,
        ),
        User(
            username="user6",
            email="user6@email.com",
            hashed_password=hash_password("User6Pass!"),
            is_private=False,
        ),
    ]

    session.add_all(users)
    session.flush()  # ensure user IDs exist

    follows = [
        # user1 follows user2 and user3
        Follow(follower_id=users[0].id, followee_id=users[1].id, accepted=True),
        Follow(follower_id=users[0].id, followee_id=users[2].id, accepted=True),
        # user2 follows user3
        Follow(follower_id=users[1].id, followee_id=users[2].id, accepted=True),
        # user5 sends follow requests (not accepted)
        Follow(follower_id=users[4].id, followee_id=users[0].id, accepted=False),
        Follow(follower_id=users[4].id, followee_id=users[5].id, accepted=False),
    ]

    session.add_all(follows)
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
def test_users_with_posts(session: Session):
    """
    Creates:
    - user_with_many_posts (3 posts)
    - user_with_single_post (1 post)
    - user_without_posts (0 posts)
    """

    users = [
        User(
            username="manyposts",
            email="manyposts@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
        User(
            username="singlepost",
            email="singlepost@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
        User(
            username="noposts",
            email="noposts@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
    ]

    session.add_all(users)
    session.flush()  # ensures user IDs are available

    posts = [
        # many posts user
        Post(title="Post 1", content="Content 1", owner_id=users[0].id),
        Post(title="Post 2", content="Content 2", owner_id=users[0].id),
        Post(title="Post 3", content="Content 3", owner_id=users[0].id),
        # single post user
        Post(title="Only Post", content="Single content", owner_id=users[1].id),
    ]

    session.add_all(posts)
    session.commit()

    return {
        "user_with_many_posts": users[0],
        "user_with_single_post": users[1],
        "user_without_posts": users[2],
    }
