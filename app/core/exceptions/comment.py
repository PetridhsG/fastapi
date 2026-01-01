from fastapi import status

from app.core.exceptions.base_exception import AppBaseException


class CommentBaseException(AppBaseException):
    """Base class for all comment-related exceptions."""

    error: str = "comment_error"
    message: str = "A comment error occurred."


class CommentNotFound(CommentBaseException):
    """Exception raised when a comment is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error: str = "comment_not_found"
    message: str = "The requested comment was not found."


class CommentUserNotAllowed(CommentBaseException):
    """Exception raised when a user is not allowed to modify a comment."""

    status_code = status.HTTP_403_FORBIDDEN
    error: str = "comment_user_not_allowed"
    message: str = "You do not have permission to modify this comment."
