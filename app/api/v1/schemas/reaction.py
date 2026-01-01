from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.user import UserListItemOut
from app.db.models.reaction import ReactionType


class ReactionCreate(BaseModel):
    """Schema for creating a new reaction."""

    type: ReactionType


class ReactionCreatedOut(BaseModel):
    """Schema for reaction data returned after creation."""

    type: ReactionType
    post_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ReactionOut(BaseModel):
    """Schema for reaction data returned in responses."""

    post_id: int
    user_id: int
    type: ReactionType
    owner: UserListItemOut

    model_config = ConfigDict(from_attributes=True)


class ReactionEdit(BaseModel):
    """Schema for editing a reaction."""

    type: ReactionType | None = None
