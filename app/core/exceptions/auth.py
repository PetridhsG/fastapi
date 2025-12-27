from fastapi import status


class AuthBaseException(Exception):
    """Base class for all auth-related exceptions."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error: str = "auth_error"
    message: str = "An authentication error occurred."

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


class AuthInvalidLoginCredentials(AuthBaseException):
    """Raised when the provided login credentials are invalid."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error = "invalid_login"
    message = "Invalid login credentials."


class AuthInvalidJWT(AuthBaseException):
    """Raised when the provided JWT cannot be validated or is invalid."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error = "invalid_jwt"
    message = "JWT is invalid or cannot be validated."
