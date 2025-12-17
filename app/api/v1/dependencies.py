from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions.user import UserNotFound
from app.core.security.jwt import verify_access_token
from app.db.database import get_db
from app.db.models import User
from app.services.auth import AuthService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    token_data = verify_access_token(token)

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise UserNotFound

    return user


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
