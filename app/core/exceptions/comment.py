from app.core.exceptions.base_exception import AppBaseException


class CommentBaseException(AppBaseException):
    """Base class for all comment-related exceptions."""

    error: str = "comment_error"
    message: str = "A comment error occurred."
