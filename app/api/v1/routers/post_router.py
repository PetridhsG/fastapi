from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_current_user, get_post_service
from app.api.v1.schemas.post import PostCreate, PostCreatedOut
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
