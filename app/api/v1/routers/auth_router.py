from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import get_auth_service
from app.api.v1.schemas.auth import Token
from app.services.auth_service import AuthService

prefix = "/auth"
router = APIRouter(prefix=prefix, tags=["Authentication"])


@router.post(
    "/login", response_model=Token, summary="User login to obtain access token"
)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login_user(user_credentials)
