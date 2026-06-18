from flask import Blueprint, jsonify, request

from app.services.auth_service import (
    ServiceError,
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