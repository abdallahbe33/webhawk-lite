from app.repositories.security_log_repository import create_log
from app.security.request_scanner import scan_values


def scan_request_data(path, query, body, headers=None):
    data_to_scan = {
        "path": path,
        "query": query,
        "body": body,
    }

    if headers:
        data_to_scan["headers"] = headers

    return scan_values(data_to_scan)


def save_security_log(
    backend_id,
    ip_address,
    method,
    endpoint,
    scan_result,
    request_data
):
    return create_log(
        backend_id=backend_id,
        ip_address=ip_address,
        method=method,
        endpoint=endpoint,
        attack_type=scan_result.get("attack_type"),
        is_blocked=not scan_result.get("allowed", True),
        request_data=request_data
    )