from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_current_user, get_user_service
from app.api.v1.schemas.user import UserCreate, UserOut
from app.core.exceptions.user import (
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotFound,
)
from app.services.user_service import UserService

prefix = "/users"
router = APIRouter(prefix=prefix, tags=["Users"])


@router.post(
    "",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        new_user = user_service.create_user(user)

    except UserEmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "user_email_already_exists",
                "message": "A user with this email already exists.",
                "field": "email",
            },
        )

    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "username_already_exists",
                "message": "This username is already taken.",
                "field": "username",
            },
        )

    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "user_creation_failed",
                "message": "Unable to create user.",
            },
        )

    return new_user


@router.get(
    "/{user_id}",
    summary="Get user by ID",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
):
    print(f"Current user ID: {current_user.id}")
    try:
        user = user_service.get_user(user_id)
    except UserNotFound:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "user_not_found", "message": "User not found."},
        )
    return user
