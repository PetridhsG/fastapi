from app.core.exceptions.base_exception import AppBaseException


class FollowBaseException(AppBaseException):
    """Base class for all follow-related exceptions."""

    error: str = "follow_error"
    message: str = "A follow error occurred."
