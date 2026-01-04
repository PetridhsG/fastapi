import pytest
from sqlalchemy.orm import Session

from app.core.security.password import hash_password
from app.db.models.comment import Comment
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


@pytest.fixture(scope="function")
def test_users_with_posts_comments(session: Session):
    """
    Creates:

    Users:
    - user1: 2 posts
        - post1: 2 comments (by user2)
        - post2: 0 comments
    - user2: 1 post
        - post3: 1 comment (by user1)
    - user3: no posts
    """

    users = {
        "user_with_two_posts": User(
            username="user1comments",
            email="user1comments@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
        "user_with_one_post": User(
            username="user2comments",
            email="user2comments@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
        "user_without_posts": User(
            username="user3comments",
            email="user3comments@example.com",
            hashed_password=hash_password("Pass123!"),
            is_private=False,
        ),
    }

    session.add_all(users.values())
    session.flush()

    posts = [
        # user1 posts
        Post(
            title="User1 Post 1",
            content="Content 1",
            owner_id=users["user_with_two_posts"].id,
        ),
        Post(
            title="User1 Post 2",
            content="Content 2",
            owner_id=users["user_with_two_posts"].id,
        ),
        # user2 post
        Post(
            title="User2 Post 1",
            content="Content 3",
            owner_id=users["user_with_one_post"].id,
        ),
    ]

    session.add_all(posts)
    session.flush()

    comments = [
        # user2 comments on user1 post1
        Comment(
            content="Nice post!",
            post_id=posts[0].id,
            owner_id=users["user_with_one_post"].id,
        ),
        Comment(
            content="I agree!",
            post_id=posts[0].id,
            owner_id=users["user_with_one_post"].id,
        ),
        # user1 comments on user2 post
        Comment(
            content="Thanks for sharing",
            post_id=posts[2].id,
            owner_id=users["user_with_two_posts"].id,
        ),
    ]

    session.add_all(comments)
    session.commit()

    return users
