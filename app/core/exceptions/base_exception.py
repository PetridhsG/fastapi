from fastapi import status


class AppBaseException(Exception):
    """Base class for all application exceptions."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error: str = "error"
    message: str = "An error occurred."
    field: str = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)
