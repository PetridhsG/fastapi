from app.core.exceptions.base_exception import AppBaseException


class ReactionBaseException(AppBaseException):
    """Base class for all reaction-related exceptions."""

    error: str = "reaction_error"
    message: str = "A reaction error occurred."
