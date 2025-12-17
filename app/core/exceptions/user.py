class UserEmailAlreadyExists(Exception):
    """Raised when a user with the given email already exists when trying to create a new user."""

    pass


class UserNotFound(Exception):
    """Raised when a user is not found in the database."""

    pass
