from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.exceptions.auth import AuthInvalidLoginCredentials
from app.core.security.jwt import create_access_token
from app.core.security.password import verify_password
from app.db.models import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, user_credentials: OAuth2PasswordRequestForm):
        """Authenticate user and return access token; raises InvalidLoginCredentials on failure."""
        user = (
            self.db.query(User).filter(User.email == user_credentials.username).first()
        )

        if not user:
            raise AuthInvalidLoginCredentials()

        if not verify_password(user_credentials.password, user.hashed_password):
            raise AuthInvalidLoginCredentials()

        access_token = create_access_token(data={"user_id": user.id})

        return {"access_token": access_token, "token_type": "bearer"}
