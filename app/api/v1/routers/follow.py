from fastapi import APIRouter

prefix = "/follow"
router = APIRouter(prefix=prefix, tags=["Follows"])


@router.get("/")
def get_follows():
    return {"message": "ok"}
