import re

import bcrypt
from app.repositories.user_repository import (
    create_user,
    find_by_email,
    find_by_id,
)


import hashlib
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

from app.repositories.session_repository import (
    create_session,
    find_active_session,
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


def login_user(data, ip_address):
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    user = find_by_email(email)

    if not user:
        raise ServiceError(
            "Invalid email or password",
            status_code=401,
        )

    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    )

    if not password_matches:
        raise ServiceError(
            "Invalid email or password",
            status_code=401,
        )

    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        hours=current_app.config[
            "JWT_EXPIRATION_HOURS"
        ]
    )

    payload = {
        "sub": str(user.id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    token_hash = hash_token(token)
    create_session(
        user_id=user.id,
        token_hash=token_hash,
        ip_address=ip_address,
        expires_at=expires_at,
    )

    return user, token, expires_at
def hash_token(token):
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()
def authenticate_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as error:
        raise ServiceError(
            "Token has expired",
            status_code=401,
        ) from error
    except jwt.InvalidTokenError as error:
        raise ServiceError(
            "Invalid token",
            status_code=401,
        ) from error

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as error:
        raise ServiceError(
            "Invalid token payload",
            status_code=401,
        ) from error

    session = find_active_session(
        hash_token(token)
    )

    if not session:
        raise ServiceError(
            "Session is inactive or expired",
            status_code=401,
        )

    if session.user_id != user_id:
        raise ServiceError(
            "Token does not match its session",
            status_code=401,
        )

    user = find_by_id(user_id)

    if not user:
        raise ServiceError(
            "User no longer exists",
            status_code=401,
        )

    return user, session
