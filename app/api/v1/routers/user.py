from fastapi import APIRouter

prefix = "/users"
router = APIRouter(prefix=prefix, tags=["Users"])


@router.get("/")
def get_users():
    return {"message": "ok"}
