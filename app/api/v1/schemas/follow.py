from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FollowRequestOut(BaseModel):
    """Schema for follow request data returned in lists (user follow requests)."""

    follower_id: int
    follower_username: str
    followee_id: int
    followee_username: str
    created_at: datetime
    accepted: bool

    model_config = ConfigDict(from_attributes=True)
