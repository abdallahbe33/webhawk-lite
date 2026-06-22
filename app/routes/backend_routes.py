from flask import Blueprint, g, jsonify, request

from app.services.backend_service import (
    BackendServiceError,
    disable_owned_backend,
    get_owned_backend,
    get_user_backends,
    register_backend,
    update_owned_backend,
)
from app.utils.auth import jwt_required


backend_bp = Blueprint("backends", __name__)


@backend_bp.post("")
@jwt_required
def create():
    data = request.get_json(silent=True) or {}

    try:
        backend = register_backend(
            g.current_user.id,
            data,
        )
    except BackendServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        message="Backend registered successfully",
        backend=backend.to_dict(),
    ), 201


@backend_bp.get("")
@jwt_required
def list_all():
    backends = get_user_backends(
        g.current_user.id
    )

    return jsonify(
        count=len(backends),
        backends=[
            backend.to_dict()
            for backend in backends
        ],
    )
@backend_bp.get("/<int:backend_id>")
@jwt_required
def get_one(backend_id):
    try:
        backend = get_owned_backend(
            backend_id,
            g.current_user.id,
        )
    except BackendServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        backend=backend.to_dict()
    )


@backend_bp.put("/<int:backend_id>")
@jwt_required
def update(backend_id):
    data = request.get_json(silent=True) or {}

    try:
        backend = update_owned_backend(
            backend_id,
            g.current_user.id,
            data,
        )
    except BackendServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        message="Backend updated successfully",
        backend=backend.to_dict(),
    )


@backend_bp.delete("/<int:backend_id>")
@jwt_required
def disable(backend_id):
    try:
        backend = disable_owned_backend(
            backend_id,
            g.current_user.id,
        )
    except BackendServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        message="Backend disabled successfully",
        backend=backend.to_dict(),
    )