from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_comment_service
from app.core.security.access_controls import get_current_user
from app.services.comment_service import CommentService

prefix = "/posts/{post_id}/comments"
router = APIRouter(prefix=prefix, tags=["Comments"])


@router.get(
    "",
    summary="Get comments for a post",
    status_code=None,  # Replace None with the appropriate status code
)
def get_post_comments(
    post_id: int,
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    return comment_service.get_post_comments(current_user.id, post_id)


@router.post(
    "",
    summary="Add a comment to a post",
    status_code=None,  # Replace None with the appropriate status code
)
def add_post_comment(
    post_id: int,
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    comment_service.add_post_comment(current_user.id, post_id)


@router.patch(
    "/{comment_id}",
    summary="Update a comment to a post",
    status_code=None,  # Replace None with the appropriate status code
)
def update_post_comment(
    post_id: int,
    comment_id: int,
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    comment_service.update_post_comment(current_user.id, post_id, comment_id)


@router.delete(
    "/{comment_id}",
    summary="Delete a comment from a post",
    status_code=None,  # Replace None with the appropriate status code
)
def delete_post_comment(
    post_id: int,
    comment_id: int,
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    comment_service.delete_post_comment(current_user.id, post_id, comment_id)
