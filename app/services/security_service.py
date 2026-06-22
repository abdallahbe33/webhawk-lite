from app.security.request_scanner import (
    scan_request_sources,
)


def scan_request_data(data):
    path = data.get("path", "")
    query = data.get("query", {})
    body = data.get("body", {})

    return scan_request_sources(
        path=path,
        query=query,
        body=body,
    )