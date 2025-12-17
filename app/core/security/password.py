import re

from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(v: str) -> str:
    if (
        len(v) < 6
        or not re.search(r"[A-Z]", v)
        or not re.search(r"[0-9]", v)
        or not re.search(r"[^\w\s]", v)
    ):
        raise ValueError(
            "Password must be at least 6 characters long and contain "
            "one uppercase letter, one number, and one special character."
        )
    return v
