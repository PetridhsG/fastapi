from typing import List

from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_follow_service
from app.api.v1.schemas.follow import FollowRequestOut
from app.core.security.access_controls import get_current_user
from app.services.follow_service import FollowService

prefix = "/follows"
router = APIRouter(prefix=prefix, tags=["Follows"])


@router.post(
    "/{user_id}/follow",
    summary="Follow a user",
    status_code=status.HTTP_204_NO_CONTENT,
)
def follow_user(
    user_id: int,
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    follow_service.follow_user(follower_id=current_user.id, followee_id=user_id)


@router.delete(
    "/{user_id}/follow",
    summary="Unfollow a user or remove follow request",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unfollow_user(
    user_id: int,
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    follow_service.unfollow_user(follower_id=current_user.id, followee_id=user_id)


@router.delete(
    "/{user_id}/follower",
    summary="Remove a user from your followers list",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_follower(
    user_id: int,
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    follow_service.unfollow_user(follower_id=user_id, followee_id=current_user.id)


@router.get(
    "/requests/incoming",
    summary="Get incoming follow requests",
    response_model=List[FollowRequestOut],
)
def get_incoming_follow_requests(
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    return follow_service.get_follow_requests(user_id=current_user.id, incoming=True)


@router.get(
    "/requests/outgoing",
    summary="Get outgoing follow requests",
    response_model=List[FollowRequestOut],
)
def get_outgoing_follow_requests(
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    return follow_service.get_follow_requests(user_id=current_user.id, incoming=False)


@router.patch(
    "/{user_id}/accept",
    summary="Accept a follow request",
    status_code=status.HTTP_204_NO_CONTENT,
)
def accept_follow_request(
    user_id: int,
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    follow_service.accept_follow_request(
        follower_id=user_id, followee_id=current_user.id
    )


@router.delete(
    "/{user_id}/reject",
    summary="Accept a follow request",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reject_follow_request(
    user_id: int,
    current_user=Depends(get_current_user),
    follow_service: FollowService = Depends(get_follow_service),
):
    follow_service.reject_follow_request(
        follower_id=user_id, followee_id=current_user.id
    )
