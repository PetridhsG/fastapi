import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.core.security.password import validate_password


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def oassword_strength(cls, v: str) -> str:
        return validate_password(v)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
