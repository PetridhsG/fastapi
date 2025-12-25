from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_current_user, get_user_service
from app.api.v1.schemas.user import (
    UserChangePassword,
    UserCreate,
    UserCreatedOut,
    UserEdit,
    UserEditOut,
    UserListItemOut,
    UserPublicOut,
    UserSettingsOut,
)
from app.services.user_service import UserService

prefix = "/users"
router = APIRouter(prefix=prefix, tags=["Users"])


@router.post(
    "",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreatedOut,
)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(user)


@router.get(
    "/me",
    summary="Get current user",
    response_model=UserPublicOut,
)
def get_logged_in_user(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_current_user(current_user.id)


@router.get(
    "/me/settings",
    summary="Get current user settings",
    response_model=UserSettingsOut,
)
def get_current_user_settings(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_current_user_settings(current_user.id)


@router.get(
    "",
    summary="Search users by username",
    response_model=List[UserListItemOut],
)
def search_users(
    query: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.search_users(current_user.id, query)


@router.get(
    "/{username}",
    summary="Get public user information by username",
    response_model=UserPublicOut,
)
def get_user_by_username(
    username: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user_by_username(current_user.id, username)


@router.get(
    "/{username}/followers",
    summary="Get a list of followers for a user",
    response_model=List[UserListItemOut],
)
def get_user_followers(
    username: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    return user_service.get_user_followers(
        current_user.id, username, limit=limit, offset=offset, search=search
    )


@router.get(
    "/{username}/following",
    summary="Get a list of following for a user",
    response_model=List[UserListItemOut],
)
def get_user_following(
    username: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    return user_service.get_user_following(
        current_user.id, username, limit=limit, offset=offset, search=search
    )


@router.get(
    "/{username}/posts",
    summary="Get current user's posts",
    response_model=UserPublicOut,
)
def get_user_posts(
    username: str,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user_posts(current_user.id, username)


@router.patch(
    "/me",
    summary="Edit current user's information",
    response_model=UserEditOut,
)
def edit_current_user(
    user_edit: UserEdit,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user(current_user.id, user_edit)


@router.put(
    "/me/password",
    summary="Change current user's password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_password(
    data: UserChangePassword,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.change_password(current_user.id, data)


@router.delete(
    "/me",
    summary="Delete current user",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_current_user(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(current_user.id)
