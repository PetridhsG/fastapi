from fastapi import APIRouter

from .routers import (
    auth_router,
    comment_router,
    follow_router,
    post_router,
    reaction_router,
    user_router,
)

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(user_router.router)
router.include_router(post_router.router)
router.include_router(comment_router.router)
router.include_router(follow_router.router)
router.include_router(reaction_router.router)
