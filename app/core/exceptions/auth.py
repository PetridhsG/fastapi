from fastapi import status

from app.core.exceptions.base_exception import AppBaseException


class AuthBaseException(AppBaseException):
    """Base class for all auth-related exceptions."""

    error: str = "auth_error"
    message: str = "An authentication error occurred."


class AuthInvalidLoginCredentials(AuthBaseException):
    """Raised when the provided login credentials are invalid."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error = "invalid_login_credentials"
    message = "Invalid login credentials."


class AuthInvalidJWT(AuthBaseException):
    """Raised when the provided JWT cannot be validated or is invalid."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error = "invalid_jwt"
    message = "JWT is invalid or cannot be validated."


class AuthUserCannotBeAuthenticated(AuthBaseException):
    """Raised when the user cannot be authenticated from the provided token."""

    status_code = status.HTTP_400_BAD_REQUEST
    error = "user_cannot_be_authenticated"
    message = "The user is not authenticated or cannot be found in the database."
