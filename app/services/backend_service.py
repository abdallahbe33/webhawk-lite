import secrets
from urllib.parse import urlparse

from app.repositories.backend_repository import (
    create_backend,
    find_owned_backend,
    list_backends_by_user,
    save_backend,
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
def get_owned_backend(backend_id, user_id):
    backend = find_owned_backend(
        backend_id,
        user_id,
    )

    if not backend:
        raise BackendServiceError(
            "Backend not found",
            status_code=404,
        )

    return backend


def update_owned_backend(
    backend_id,
    user_id,
    data,
):
    backend = get_owned_backend(
        backend_id,
        user_id,
    )

    if "service_name" in data:
        service_name = str(
            data["service_name"]
        ).strip()

        if not service_name:
            raise BackendServiceError(
                "Service name cannot be empty"
            )

        backend.service_name = service_name

    if "target_url" in data:
        target_url = str(
            data["target_url"]
        ).strip().rstrip("/")

        if not is_valid_target_url(target_url):
            raise BackendServiceError(
                "A valid HTTP or HTTPS target URL is required"
            )

        backend.target_url = target_url

    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            raise BackendServiceError(
                "is_active must be true or false"
            )

        backend.is_active = data["is_active"]

    return save_backend(backend)


def disable_owned_backend(backend_id, user_id):
    backend = get_owned_backend(
        backend_id,
        user_id,
    )

    backend.is_active = False

    return save_backend(backend)
