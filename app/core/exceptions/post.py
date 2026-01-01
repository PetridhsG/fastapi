from fastapi import status

from app.core.exceptions.base_exception import AppBaseException


class PostBaseException(AppBaseException):
    """Base class for all follow-related exceptions."""

    error: str = "post_error"
    message: str = "A post error occurred."


class PostNotFound(PostBaseException):
    """Exception raised when a post is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error: str = "post_not_found"
    message: str = "The requested post was not found."


class PostUserNotAllowed(PostBaseException):
    """Exception raised when a user is not allowed to access a post."""

    status_code = status.HTTP_403_FORBIDDEN
    error: str = "post_user_not_allowed"
    message: str = "The user is not allowed to make changes to this post."
