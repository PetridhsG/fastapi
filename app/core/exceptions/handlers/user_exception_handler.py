from fastapi import HTTPException, status

from app.core.exceptions.user import (
    InvalidPassword,
    PasswordUnchanged,
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotAllowed,
    UserNotFound,
)


def handle_user_exception(exc: Exception):
    """Map user service exceptions to HTTPException responses."""
    if isinstance(exc, UserEmailAlreadyExists):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "user_email_already_exists",
                "message": "A user with this email already exists.",
                "field": "email",
            },
        )
    if isinstance(exc, UsernameAlreadyExists):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "username_already_exists",
                "message": "This username is already taken.",
                "field": "username",
            },
        )
    if isinstance(exc, UserAlreadyExists):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "user_creation_failed",
                "message": "Unable to create user.",
            },
        )
    if isinstance(exc, UserNotFound):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "user_not_found",
                "message": "User not found.",
            },
        )
    if isinstance(exc, UserNotAllowed):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "user_not_allowed",
                "message": "You are not allowed to perform this action.",
            },
        )
    if isinstance(exc, InvalidPassword):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_password",
                "message": "Current password is incorrect.",
                "field": "current_password",
            },
        )
    if isinstance(exc, PasswordUnchanged):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "password_unchanged",
                "message": "New password cannot be the same as the current password.",
                "field": "new_password",
            },
        )

    raise exc
