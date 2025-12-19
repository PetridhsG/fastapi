from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import get_auth_service
from app.api.v1.schemas.auth import Token
from app.core.exceptions.auth import InvalidLoginCredentials
from app.services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login", response_model=Token, summary="User login to obtain access token"
)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        auth_token = auth_service.login_user(user_credentials)
    except InvalidLoginCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_login_credentials",
                "message": "Invalid login credentials provided.",
            },
        )

    return auth_token
