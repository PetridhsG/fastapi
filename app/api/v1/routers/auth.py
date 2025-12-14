from fastapi import APIRouter

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login_user():
    return {"status": "ok"}
