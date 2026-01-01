from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.user import UserListItemOut


class CommentCreate(BaseModel):
    """Schema for creating a new comment."""

    content: str


class CommentCreateOut(BaseModel):
    """Schema for comment data returned after creation."""

    id: int
    content: str
    created_at: datetime
    post_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentOut(BaseModel):
    """Schema for comment data returned in responses."""

    id: int
    content: str
    created_at: datetime
    post_id: int
    owner: UserListItemOut

    model_config = ConfigDict(from_attributes=True)


class CommentEdit(BaseModel):
    """Schema for editing a comment."""

    content: str | None = None
