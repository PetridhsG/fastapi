from typing import List

from sqlalchemy.orm import Session

from app.api.v1.schemas.follow import FollowRequestOut
from app.core.exceptions.follow import (
    FollowAlreadyAccepted,
    FollowAlreadyExists,
    FollowNotAccepted,
    FollowNotFound,
    FollowYourself,
)
from app.db.models.follow import Follow
from app.services.helpers.user_helper import UserHelper


class FollowService:
    def __init__(self, db: Session):
        self.db = db
        self.user_helper = UserHelper(db)

    def follow_user(self, follower_id: int, followee_id: int) -> None:
        """Create a follow relationship between two users."""

        if follower_id == followee_id:
            raise FollowYourself()

        followee = self.user_helper.get_user_by_id(followee_id)

        follow = self.db.get(Follow, (follower_id, followee_id))
        if follow:
            raise FollowAlreadyExists()

        # Auto-accept public users
        accepted = not followee.is_private

        follow = Follow(
            follower_id=follower_id,
            followee_id=followee_id,
            accepted=accepted,
        )

        self.db.add(follow)
        self.db.flush()

    def unfollow_user(self, follower_id: int, followee_id: int) -> None:
        """Remove a follow relationship between two users."""

        follow = self._get_follow(follower_id, followee_id)

        if not follow.accepted:
            raise FollowNotAccepted()

        self.db.delete(follow)
        self.db.flush()

    def accept_follow_request(self, follower_id: int, followee_id: int) -> None:
        """Accept a follow request."""

        follow = self._get_follow(follower_id, followee_id)

        if follow.accepted:
            raise FollowAlreadyAccepted()

        follow.accepted = True
        self.db.flush()

    def remove_pending_request(self, follower_id: int, followee_id: int) -> None:
        """Remove a pending follow request, either by sender or recipient."""

        follow = self._get_follow(follower_id, followee_id)

        if follow.accepted:
            raise FollowAlreadyAccepted()

        self.db.delete(follow)
        self.db.flush()

    def get_follow_requests(
        self, user_id: int, incoming: bool = True
    ) -> List[FollowRequestOut]:
        """Get all follow requests sent to the user or by the user."""

        if incoming:
            filter_condition = Follow.followee_id == user_id
        else:
            filter_condition = Follow.follower_id == user_id

        follows = (
            self.db.query(Follow)
            .filter(filter_condition, Follow.accepted.is_(False))
            .order_by(Follow.created_at.desc())
            .all()
        )

        return [
            FollowRequestOut(
                follower_id=f.follower_id,
                follower_username=f.follower.username,
                followee_id=f.followee_id,
                followee_username=f.followee.username,
                created_at=f.created_at,
                accepted=f.accepted,
            )
            for f in follows
        ]

    def _get_follow(self, follower_id: int, followee_id: int) -> Follow:
        """Internal helper to fetch a follow relationship."""
        if follower_id == followee_id:
            raise FollowYourself()

        follow = self.db.get(Follow, (follower_id, followee_id))

        if not follow:
            raise FollowNotFound()
        return follow
