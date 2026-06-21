import secrets
from urllib.parse import urlparse

from app.repositories.backend_repository import (
    create_backend,
    list_backends_by_user,
)


class BackendServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)

        self.message = message
        self.status_code = status_code


def is_valid_target_url(target_url):
    parsed_url = urlparse(target_url)

    return (
        parsed_url.scheme in {"http", "https"}
        and bool(parsed_url.netloc)
        and parsed_url.username is None
        and parsed_url.password is None
    )


def register_backend(user_id, data):
    service_name = str(
        data.get("service_name", "")
    ).strip()

    target_url = str(
        data.get("target_url", "")
    ).strip().rstrip("/")

    if not service_name:
        raise BackendServiceError(
            "Service name is required"
        )

    if not is_valid_target_url(target_url):
        raise BackendServiceError(
            "A valid HTTP or HTTPS target URL is required"
        )

    api_key = (
        "webhawk_"
        + secrets.token_urlsafe(24)
    )

    return create_backend(
        user_id=user_id,
        service_name=service_name,
        target_url=target_url,
        api_key=api_key,
    )


def get_user_backends(user_id):
    return list_backends_by_user(user_id)