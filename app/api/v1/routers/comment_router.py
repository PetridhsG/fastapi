from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies import get_comment_service
from app.api.v1.schemas.comment import (
    CommentCreate,
    CommentCreatedOut,
    CommentEdit,
    CommentOut,
)
from app.core.security.access_controls import can_view_post, get_current_user
from app.services.comment_service import CommentService

prefix = "/posts/{post_id}/comments"
router = APIRouter(prefix=prefix, tags=["Comments"])


@router.post(
    "",
    summary="Add a comment to a post",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentCreatedOut,
)
def add_post_comment(
    comment: CommentCreate,
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    return comment_service.add_post_comment(current_user.id, post_id, comment)


@router.get(
    "",
    summary="Get comments for a post",
    response_model=List[CommentOut],
)
def get_post_comments(
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    return comment_service.get_post_comments(
        current_user_id=current_user.id, post_id=post_id, limit=limit, offset=offset
    )


@router.patch(
    "/{comment_id}",
    summary="Update a comment to a post",
    response_model=CommentCreatedOut,
)
def update_post_comment(
    comment: CommentEdit,
    comment_id: int,
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    return comment_service.update_post_comment(
        current_user.id, post_id, comment_id, comment
    )


@router.delete(
    "/{comment_id}",
    summary="Delete a comment from a post",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post_comment(
    comment_id: int,
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    comment_service.delete_post_comment(current_user.id, post_id, comment_id)
