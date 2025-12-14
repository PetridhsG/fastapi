from fastapi import APIRouter

prefix = "/reactions"
router = APIRouter(prefix=prefix, tags=["Reactions"])


@router.get("/")
def get_reactions():
    return {"message": "ok"}
