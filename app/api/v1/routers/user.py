from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_user_service
from app.api.v1.schemas.user import UserCreate, UserOut
from app.core.exceptions.user import UserEmailAlreadyExists
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
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = user_service.create_user(user)
    except UserEmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "UserEmailAlreadyExists",
                "message": "A user with this email already exists.",
                "field": "email",
            },
        )

    return new_user
