from fastapi import status

from app.core.exceptions.base_exception import AppBaseException


class FollowBaseException(AppBaseException):
    """Base class for all follow-related exceptions."""

    error: str = "follow_error"
    message: str = "A follow error occurred."


class FollowYourself(FollowBaseException):
    """Raised when a user attempts to follow themselves."""

    status_code = status.HTTP_400_BAD_REQUEST
    error: str = "follow_yourself"
    message: str = "You cannot do follow related actions on yourself."


class FollowAlreadyExists(FollowBaseException):
    """Raised when a follow relationship already exists."""

    status_code = status.HTTP_409_CONFLICT
    error: str = "follow_already_exists"
    message: str = "The follow relationship already exists."


class FollowNotFound(FollowBaseException):
    """Raised when a follow relationship is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error: str = "follow_not_found"
    message: str = "The follow relationship was not found."


class FollowNotAccepted(FollowBaseException):
    """Raised when a follow relationship is not accepted."""

    status_code = status.HTTP_403_FORBIDDEN
    error: str = "follow_not_accepted"
    message: str = "The follow relationship is not accepted so it cannot be removed."


class FollowAlreadyAccepted(FollowBaseException):
    """Raised when a follow relationship is already accepted."""

    status_code = status.HTTP_409_CONFLICT
    error: str = "follow_already_accepted"
    message: str = "The follow relationship is already accepted."
