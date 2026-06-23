from flask import Blueprint, g, jsonify, request

from app.repositories.security_log_repository import get_logs_for_user
from app.services.security_service import scan_request_data, save_security_log
from app.utils.auth import jwt_required

security_bp = Blueprint("security", __name__)


@security_bp.post("/security/scan")
@jwt_required
def manual_scan():
    payload = request.get_json(silent=True) or {}

    path = payload.get("path", "")
    query = payload.get("query", {})
    body = payload.get("body", {})
    headers = payload.get("headers", {})
    backend_id = payload.get("backend_id")

    result = scan_request_data(path, query, body, headers)

    if backend_id:
        save_security_log(
            backend_id=backend_id,
            ip_address=request.remote_addr or "unknown",
            method="MANUAL",
            endpoint=path,
            scan_result=result,
            request_data={
                "path": path,
                "query": query,
                "body": body,
                "headers": headers
            }
        )

    status_code = 200 if result["allowed"] else 403

    return jsonify(result), status_code


@security_bp.get("/logs/security")
@jwt_required
def security_logs():
    blocked_only = request.args.get("blocked_only", "false").lower() == "true"

    try:
        limit = int(request.args.get("limit", 100))
    except ValueError:
        return jsonify(error="limit must be a number"), 400

    logs = get_logs_for_user(
        user_id=g.current_user.id,
        blocked_only=blocked_only,
        limit=limit
    )

    return jsonify(
        count=len(logs),
        logs=[log.to_dict() for log in logs]
    )