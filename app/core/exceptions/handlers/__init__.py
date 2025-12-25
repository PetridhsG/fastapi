from fastapi import FastAPI, Request

from app.core.exceptions.auth import InvalidLoginCredentials
from app.core.exceptions.handlers.auth_exception_handler import handle_auth_exception
from app.core.exceptions.handlers.user_exception_handler import handle_user_exception
from app.core.exceptions.user import (
    InvalidPassword,
    PasswordUnchanged,
    UserAlreadyExists,
    UserEmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotAllowed,
    UserNotFound,
)


def register_user_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExists)
    @app.exception_handler(UserEmailAlreadyExists)
    @app.exception_handler(UsernameAlreadyExists)
    @app.exception_handler(UserNotFound)
    @app.exception_handler(UserNotAllowed)
    @app.exception_handler(InvalidPassword)
    @app.exception_handler(PasswordUnchanged)
    async def user_exception_handler(request: Request, exc: Exception):
        return handle_user_exception(exc)


def register_auth_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidLoginCredentials)
    async def auth_exception_handler(request: Request, exc: Exception):
        return handle_auth_exception(exc)
