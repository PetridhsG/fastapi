from datetime import datetime
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field

from app.api.v1.schemas.user import UserListItemOut
from app.core.enums import ReactionType


class PostCreate(BaseModel):
    """Schema for creating a new post."""

    title: str = Field(
        ...,
        min_length=4,
        max_length=40,
        description="Post title must be between 4 and 40 characters",
    )
    content: str


class PostCreatedOut(BaseModel):
    """Schema for post data returned upon successful creation."""

    id: int
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListItemOut(BaseModel):
    """Schema for post data returned in lists (user posts)."""

    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    comments_count: int
    reactions_count: int
    user_reacted: ReactionType | None = None

    model_config = ConfigDict(from_attributes=True)


class PostOut(PostListItemOut):
    """Schema for post data returned when fetching a single post."""

    owner: UserListItemOut
    reactions_by_type: Dict[ReactionType, int]

    model_config = ConfigDict(from_attributes=True)


class PostEdit(BaseModel):
    """Schema for editing a post."""

    title: str | None = Field(
        None,
        min_length=4,
        max_length=40,
        description="Post title must be between 4 and 40 characters",
    )
    content: str | None
