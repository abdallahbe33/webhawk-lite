from flask import Blueprint, g, jsonify, request
from app.utils.auth import jwt_required
from app.services.auth_service import (
    ServiceError,
    login_user,
    register_user,
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    try:
        user = register_user(data)
    except ServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        message="User registered successfully",
        user=user.to_dict(),
    ), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    try:
        user, token, expires_at = login_user(
            data,
            request.remote_addr or "unknown",
        )
    except ServiceError as error:
        return jsonify(
            error=error.message
        ), error.status_code

    return jsonify(
        message="Login successful",
        access_token=token,
        token_type="Bearer",
        expires_at=expires_at.isoformat(),
        user=user.to_dict(),
    )
@auth_bp.get("/me")
@jwt_required
def current_user():
    return jsonify(
        user=g.current_user.to_dict()
    )