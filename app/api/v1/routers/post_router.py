from fastapi import APIRouter

prefix = "/posts"
router = APIRouter(prefix=prefix, tags=["Posts"])


@router.get("/")
def get_posts():
    return {"message": "ok"}
