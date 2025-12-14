from fastapi import APIRouter

prefix = "/comments"
router = APIRouter(prefix=prefix, tags=["Comments"])


@router.get("/")
def get_comments():
    return {"message": "ok"}
