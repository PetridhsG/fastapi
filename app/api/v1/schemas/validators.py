import re


def validate_password_strength(v: str) -> str:
    """Validate that the password meets complexity requirements."""
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


def validate_username(v: str | None) -> str | None:
    if v is None:
        return v
    v = v.strip()
    if len(v) < 4 or len(v) > 20 or " " in v:
        raise ValueError("Username must be 4–20 characters and contain no spaces")
    return v


def validate_bio(v: str | None) -> str | None:
    if v is None:
        return v
    v = v.strip()
    if len(v) > 200:
        raise ValueError("Bio must be at most 200 characters long")
    return v
