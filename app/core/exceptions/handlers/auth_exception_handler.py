from fastapi import HTTPException, status

from app.core.exceptions.auth import InvalidLoginCredentials


def handle_auth_exception(exc: Exception):
    """Map auth service exceptions to HTTPException responses."""
    if isinstance(exc, InvalidLoginCredentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_login_credentials",
                "message": "Invalid login credentials provided.",
            },
        )

    raise exc
