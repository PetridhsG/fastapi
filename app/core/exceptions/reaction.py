from fastapi import status

from app.core.exceptions.base_exception import AppBaseException


class ReactionBaseException(AppBaseException):
    """Base class for all reaction-related exceptions."""

    error: str = "reaction_error"
    message: str = "A reaction error occurred."


class ReactionAlreadyExists(ReactionBaseException):
    """Exception raised when a reaction already exists."""

    status_code = status.HTTP_409_CONFLICT
    error: str = "reaction_already_exists"
    message: str = "The reaction already exists."


class ReactionNotFound(ReactionBaseException):
    """Exception raised when a reaction is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error: str = "reaction_not_found"
    message: str = "The reaction was not found."
