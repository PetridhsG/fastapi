from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.api.v1.schemas.validators import (
    validate_bio,
    validate_password_strength,
    validate_username,
)


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    username: str
    password: str
    bio: str | None = None
    is_private: bool = False

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        return validate_username(v)

    @field_validator("bio")
    @classmethod
    def validate_bio(cls, v: str | None) -> str | None:
        return validate_bio(v)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return validate_password_strength(v)


class UserListItemOut(BaseModel):
    """Schema for user data returned in lists (search results,followers)."""

    id: int
    username: str
    is_following: bool
    followers_count: int

    model_config = ConfigDict(from_attributes=True)


class UserCreatedOut(BaseModel):
    """Schema for user data returned upon successful creation."""

    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    is_private: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserPublicOut(BaseModel):
    """Schema for public user data."""

    id: int
    username: str
    bio: str | None = None
    is_private: bool
    posts_count: int
    followers_count: int
    following_count: int
    is_following: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class UserSettingsOut(BaseModel):
    """Schema for user settings."""

    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    created_at: datetime
    is_private: bool

    model_config = ConfigDict(from_attributes=True)


class UserEdit(BaseModel):
    """Schema for editing user information."""

    username: str | None = None
    bio: str | None = None
    is_private: bool | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        return validate_username(v)

    @field_validator("bio")
    @classmethod
    def validate_bio(cls, v: str | None) -> str | None:
        return validate_bio(v)


class UserEditOut(BaseModel):
    """Schema for user data returned upon successful edit."""

    id: int
    username: str
    bio: str | None = None
    is_private: bool
    model_config = ConfigDict(from_attributes=True)


class UserChangePassword(BaseModel):
    """Schema for changing user password."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)
