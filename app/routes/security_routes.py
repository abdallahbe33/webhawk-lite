from flask import Blueprint, jsonify, request

from app.services.security_service import (
    scan_request_data,
)
from app.utils.auth import jwt_required


security_bp = Blueprint("security", __name__)


@security_bp.post("/scan")
@jwt_required
def scan():
    data = request.get_json(silent=True) or {}

    result = scan_request_data(data)

    status_code = (
        200
        if result["allowed"]
        else 403
    )

    return jsonify(result), status_code