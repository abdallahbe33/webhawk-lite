import re

import bcrypt

from app.repositories.user_repository import (
    create_user,
    find_by_email,
)


EMAIL_PATTERN = re.compile(
    r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
)


class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)

        self.message = message
        self.status_code = status_code


def register_user(data):
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not name:
        raise ServiceError("Name is required")

    if not EMAIL_PATTERN.match(email):
        raise ServiceError("A valid email is required")

    if len(password) < 8:
        raise ServiceError(
            "Password must contain at least 8 characters"
        )

    if find_by_email(email):
        raise ServiceError(
            "Email is already registered",
            status_code=409,
        )

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    return create_user(
        name=name,
        email=email,
        password_hash=password_hash,
    )