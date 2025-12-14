from fastapi import APIRouter

from .routers import auth, comment, follow, health, post, reaction, user

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(post.router)
router.include_router(comment.router)
router.include_router(follow.router)
router.include_router(reaction.router)
router.include_router(health.router)
