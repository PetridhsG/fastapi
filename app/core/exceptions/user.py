class UserAlreadyExists(Exception):
    """Raised when a user with the given credentials already exists when trying to create a new user."""

    pass


class UserEmailAlreadyExists(UserAlreadyExists):
    """Raised when a user with the given email already exists when trying to create a new user."""

    pass


class UsernameAlreadyExists(UserAlreadyExists):
    """Raised when a user with the given username already exists when trying to create a new user."""

    pass


class UserNotFound(Exception):
    """Raised when a user is not found in the database."""

    pass


class UserNotAllowed(Exception):
    """Raised when a user is not allowed to perform an action due to privacy settings."""

    pass


class InvalidPassword(Exception):
    """Raised when a password is invalid."""

    pass


class PasswordUnchanged(Exception):
    """Raised when the new password is the same as the current password."""

    pass
