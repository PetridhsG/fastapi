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
