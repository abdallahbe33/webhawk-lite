import requests
from flask import Blueprint, jsonify, request, Response

from app.repositories.backend_repository import find_active_by_api_key
from app.security.rate_limiter import check_rate_limit
from app.services.security_service import scan_request_data, save_security_log

proxy_bp = Blueprint("proxy", __name__)


def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr or "unknown"


def get_request_body():
    if request.is_json:
        return request.get_json(silent=True) or {}

    if request.form:
        return request.form.to_dict()

    raw_body = request.get_data(as_text=True)

    return raw_body if raw_body else {}


def get_safe_headers():
    blocked_headers = {
        "host",
        "content-length",
        "connection"
    }

    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in blocked_headers
    }


@proxy_bp.route("/<api_key>/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@proxy_bp.route("/<api_key>/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(api_key, path):
    backend = find_active_by_api_key(api_key)

    if not backend:
        return jsonify(error="Invalid or inactive API key"), 404

    ip_address = get_client_ip()
    endpoint = "/" + path

    query = request.args.to_dict()
    body = get_request_body()
    headers = get_safe_headers()

    rate_result = check_rate_limit(
        backend_id=backend.id,
        ip_address=ip_address,
        endpoint=endpoint
    )

    if not rate_result["allowed"]:
        scan_result = {
            "allowed": False,
            "attack_type": "RATE_LIMIT"
        }

        save_security_log(
            backend_id=backend.id,
            ip_address=ip_address,
            method=request.method,
            endpoint=endpoint,
            scan_result=scan_result,
            request_data={
                "query": query,
                "body": body,
                "headers": headers
            }
        )

        return jsonify(
            status="blocked",
            attack_type="RATE_LIMIT",
            message="Request blocked by rate limiter"
        ), 429

    scan_result = scan_request_data(
        path=path,
        query=query,
        body=body,
        headers=headers
    )

    if not scan_result["allowed"]:
        save_security_log(
            backend_id=backend.id,
            ip_address=ip_address,
            method=request.method,
            endpoint=endpoint,
            scan_result=scan_result,
            request_data={
                "query": query,
                "body": body,
                "headers": headers
            }
        )

        return jsonify(
            status="blocked",
            attack_type=scan_result.get("attack_type"),
            message="Request blocked by WebHawk"
        ), 403

    target_url = backend.target_url.rstrip("/") + "/" + path

    try:
        backend_response = requests.request(
            method=request.method,
            url=target_url,
            params=request.args,
            json=body if request.is_json else None,
            data=None if request.is_json else request.get_data(),
            headers=headers,
            timeout=10
        )
    except requests.RequestException:
        return jsonify(error="Target backend is unavailable"), 502

    save_security_log(
        backend_id=backend.id,
        ip_address=ip_address,
        method=request.method,
        endpoint=endpoint,
        scan_result={
            "allowed": True,
            "attack_type": None
        },
        request_data={
            "query": query,
            "body": body,
            "headers": headers
        }
    )

    return Response(
        backend_response.content,
        status=backend_response.status_code,
        content_type=backend_response.headers.get("Content-Type")
    )