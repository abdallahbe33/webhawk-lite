
from app.security.xss_detector import detect_xss
from app.security.sql_injection_detector import detect_sql_injection


def flatten_values(value, field_name=""):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            nested_name = (
                f"{field_name}.{key}"
                if field_name
                else str(key)
            )

            yield from flatten_values(
                nested_value,
                nested_name,
            )

    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            nested_name = (
                f"{field_name}[{index}]"
            )

            yield from flatten_values(
                nested_value,
                nested_name,
            )

    else:
        yield field_name, str(value)


def scan_request_sources(path, query, body):
    sql_sources = {
        "path": path,
        "query": query,
        "body": body,
    }

    for source_name, source_value in sql_sources.items():
        for field_name, value in flatten_values(
            source_value,
            source_name,
        ):
            if detect_sql_injection(value):
                return {
                    "allowed": False,
                    "attack_type": "SQL_INJECTION",
                    "field": field_name,
                    "message": (
                        "Request blocked due to "
                        "SQL Injection pattern"
                    ),
                }

    xss_sources = {
        "query": query,
        "body": body,
    }

    for source_name, source_value in xss_sources.items():
        for field_name, value in flatten_values(
            source_value,
            source_name,
        ):
            if detect_xss(value):
                return {
                    "allowed": False,
                    "attack_type": "XSS",
                    "field": field_name,
                    "message": (
                        "Request blocked due to "
                        "XSS pattern"
                    ),
                }

    return {
        "allowed": True,
        "attack_type": None,
        "field": None,
        "message": "No attack patterns detected",
    }



def scan_values(data):
    for field, value in data.items():
        text_value = str(value)

        sql_result = detect_sql_injection(text_value)
        if sql_result:
            return {
                "allowed": False,
                "attack_type": "SQL_INJECTION",
                "field": field,
                "message": "Request blocked due to SQL Injection pattern"
            }

        xss_result = detect_xss(text_value)
        if xss_result:
            return {
                "allowed": False,
                "attack_type": "XSS",
                "field": field,
                "message": "Request blocked due to XSS pattern"
            }

    return {
        "allowed": True,
        "attack_type": None,
        "field": None,
        "message": "Request is safe"
    }