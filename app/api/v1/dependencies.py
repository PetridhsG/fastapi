from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security.jwt import verify_access_token
from app.db.database import get_db
from app.db.models import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = verify_access_token(token)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise credentials_exception

    return user


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
