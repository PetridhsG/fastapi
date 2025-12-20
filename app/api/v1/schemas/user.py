import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    bio: str | None = None
    is_private: bool = False

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 4 or len(v) > 20 or " " in v:
            raise ValueError("Username must be 4–20 characters and contain no spaces")
        return v

    @field_validator("bio")
    @classmethod
    def validate_bio(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if len(v) > 200:
            raise ValueError("Bio must be at most 200 characters long")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if (
            len(v) < 6
            or not re.search(r"[A-Z]", v)
            or not re.search(r"[0-9]", v)
            or not re.search(r"[^\w\s]", v)
        ):
            raise ValueError(
                "Password must be at least 6 characters long and contain "
                "one uppercase letter, one number, and one special character."
            )
        return v


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
