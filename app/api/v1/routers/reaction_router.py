from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies import get_reaction_service
from app.api.v1.schemas.reaction import (
    ReactionCreate,
    ReactionCreatedOut,
    ReactionEdit,
    ReactionOut,
)
from app.core.security.access_controls import can_view_post, get_current_user
from app.services.reaction_service import ReactionService

prefix = "/posts/{post_id}/reactions"
router = APIRouter(prefix=prefix, tags=["Reactions"])


@router.post(
    "",
    summary="Add a reaction to a post",
    status_code=status.HTTP_201_CREATED,
    response_model=ReactionCreatedOut,
)
def add_post_reaction(
    reaction: ReactionCreate,
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.add_post_reaction(current_user.id, post_id, reaction)


@router.get(
    "",
    summary="Get reactions for a post",
    response_model=List[ReactionOut],
)
def get_post_reactions(
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.get_post_reactions(
        current_user_id=current_user.id, post_id=post_id, limit=limit, offset=offset
    )


@router.patch(
    "",
    summary="Update a reaction to a post",
    response_model=ReactionCreatedOut,
)
def update_post_reaction(
    reaction_update: ReactionEdit,
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.update_post_reaction(
        current_user.id, post_id, reaction_update
    )


@router.delete(
    "",
    summary="Delete a reaction from a post",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post_reaction(
    post_id=Depends(can_view_post),
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.delete_post_reaction(current_user.id, post_id)
