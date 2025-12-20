from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_current_user, get_user_service
from app.api.v1.schemas.user import UserCreate, UserOut, UserSearchOut
from app.core.exceptions.user import (
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
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
    "",
    summary="Search users by username",
    response_model=list[UserSearchOut],
)
def search_users(
    query: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    users = user_service.search_users(current_user.id, query)
    return users
