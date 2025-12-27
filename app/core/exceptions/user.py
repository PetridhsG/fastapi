from fastapi import status


class UserBaseException(Exception):
    """Base class for all user-related exceptions."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error: str = "user_error"
    message: str = "An unknown user error occurred."
    field: str = None  # Optional, for field-specific errors

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


class UserEmailAlreadyExists(UserBaseException):
    """Raised when a user with the given email already exists."""

    status_code = status.HTTP_409_CONFLICT
    error = "user_email_already_exists"
    message = "A user with this email already exists."
    field = "email"


class UsernameAlreadyExists(UserBaseException):
    """Raised when a user with the given username already exists."""

    status_code = status.HTTP_409_CONFLICT
    error = "username_already_exists"
    message = "This username is already taken."
    field = "username"


class UserNotFound(UserBaseException):
    """Raised when a user is not found in the database."""

    status_code = status.HTTP_404_NOT_FOUND
    error = "user_not_found"
    message = "User not found."


class UserNotAllowedToViewResource(UserBaseException):
    """Raised when a user is not allowed to view a resource."""

    status_code = status.HTTP_403_FORBIDDEN
    error = "user_not_allowed_to_view_resource"
    message = "User not allowed to view this resource."


class UserInvalidPassword(UserBaseException):
    """Raised when a password is invalid."""

    status_code = status.HTTP_400_BAD_REQUEST
    error = "invalid_password"
    message = "Current password is incorrect."
    field = "current_password"


class UserPasswordUnchanged(UserBaseException):
    """Raised when the new password is the same as the current password."""

    status_code = status.HTTP_409_CONFLICT
    error = "password_unchanged"
    message = "New password cannot be the same as the current password."
    field = "new_password"
