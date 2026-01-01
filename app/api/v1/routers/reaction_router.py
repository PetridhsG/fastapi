from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_reaction_service
from app.core.security.access_controls import get_current_user
from app.services.reaction_service import ReactionService

prefix = "/posts/{post_id}/reactions"
router = APIRouter(prefix=prefix, tags=["Reactions"])


@router.get(
    "",
    summary="Get reactions for a post",
    status_code=None,  # Replace None with the appropriate status code
)
def get_post_reactions(
    post_id: int,
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.get_post_reactions(current_user.id, post_id)


@router.post(
    "",
    summary="Add a reaction to a post",
    status_code=None,  # Replace None with the appropriate status code
)
def add_post_reaction(
    post_id: int,
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.add_post_reaction(current_user.id, post_id)


@router.delete(
    "",
    summary="Delete a reaction from a post",
    status_code=None,  # Replace None with the appropriate status code
)
def delete_post_reaction(
    post_id: int,
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.delete_post_reaction(current_user.id, post_id)


@router.patch(
    "",
    summary="Update a reaction to a post",
    status_code=None,  # Replace None with the appropriate status code
)
def update_post_reaction(
    post_id: int,
    reaction_update: None,  # Replace None with the appropriate update schema
    current_user=Depends(get_current_user),
    reaction_service: ReactionService = Depends(get_reaction_service),
):
    return reaction_service.update_post_reaction(
        current_user.id, post_id, reaction_update
    )
