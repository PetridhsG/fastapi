import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import ReactionType


class PostOut(BaseModel):
    """Schema for post data returned in responses."""

    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListItemOut(BaseModel):
    """Schema for post data returned in lists(user posts)."""

    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    comments_count: int
    reactions_count: int
    user_reacted: Optional[ReactionType] = None

    model_config = ConfigDict(from_attributes=True)
