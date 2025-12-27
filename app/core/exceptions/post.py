from app.core.exceptions.base_exception import AppBaseException


class PostBaseException(AppBaseException):
    """Base class for all follow-related exceptions."""

    error: str = "post_error"
    message: str = "A post error occurred."
