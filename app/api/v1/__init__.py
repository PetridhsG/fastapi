from fastapi import APIRouter

from .routers import (
    auth_router,
    comment_service,
    follow_service,
    post_service,
    reaction_service,
    user_service,
)

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(user_service.router)
router.include_router(post_service.router)
router.include_router(comment_service.router)
router.include_router(follow_service.router)
router.include_router(reaction_service.router)
