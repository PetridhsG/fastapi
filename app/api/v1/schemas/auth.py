from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str

    model_config = {"frozen": True}


class TokenData(BaseModel):
    """Schema for data contained in authentication token."""

    user_id: Optional[int] = None
