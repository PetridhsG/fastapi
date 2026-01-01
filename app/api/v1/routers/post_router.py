from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_post_service
from app.api.v1.schemas.post import PostCreate, PostCreatedOut, PostEdit, PostOut
from app.core.security.access_controls import (
    can_view_post,
    get_current_user,
)
from app.db.models.post import Post
from app.db.models.user import User
from app.services.post_service import PostService

prefix = "/posts"
router = APIRouter(prefix=prefix, tags=["Posts"])


@router.post(
    "",
    summary="Create a new post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostCreatedOut,
)
def create_post(
    post: PostCreate,
    current_user=Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    return post_service.create_post(current_user.id, post)


@router.get(
    "/{post_id}",
    summary="Get a post by ID",
    response_model=PostOut,
)
def get_post(
    post_id: Post = Depends(can_view_post),
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    return post_service.get_post(current_user.id, post_id)


@router.patch(
    "/{post_id}",
    summary="Update a post by ID",
    response_model=PostCreatedOut,
)
def update_post(
    post_id: int,
    post_update: PostEdit,
    current_user=Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    return post_service.update_post(current_user.id, post_id, post_update)


@router.delete(
    "/{post_id}",
    summary="Delete a post by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    current_user=Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    post_service.delete_post(current_user.id, post_id)
