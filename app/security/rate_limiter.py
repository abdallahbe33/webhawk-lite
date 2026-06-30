from datetime import datetime, timedelta

from app.repositories.rate_limit_repository import (
    find_rate_limit,
    create_rate_limit,
    save_rate_limit
)


RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_BLOCK_SECONDS = 60


def check_rate_limit(backend_id, ip_address, endpoint):
    now = datetime.utcnow()

    record = find_rate_limit(
        backend_id=backend_id,
        ip_address=ip_address,
        endpoint=endpoint
    )

    if not record:
        create_rate_limit(
            backend_id=backend_id,
            ip_address=ip_address,
            endpoint=endpoint,
            window_start=now
        )

        return {
            "allowed": True,
            "message": "Request allowed"
        }

    if record.blocked_until and record.blocked_until > now:
        return {
            "allowed": False,
            "attack_type": "RATE_LIMIT",
            "message": "Too many requests. Please try again later."
        }

    window_age = (now - record.window_start).total_seconds()

    if window_age > RATE_LIMIT_WINDOW_SECONDS:
        record.request_count = 1
        record.window_start = now
        record.blocked_until = None
        record.is_blocked = False
        save_rate_limit(record)

        return {
            "allowed": True,
            "message": "Request allowed"
        }

    record.request_count += 1

    if record.request_count > RATE_LIMIT_REQUESTS:
        record.is_blocked = True
        record.blocked_until = now + timedelta(seconds=RATE_LIMIT_BLOCK_SECONDS)
        save_rate_limit(record)

        return {
            "allowed": False,
            "attack_type": "RATE_LIMIT",
            "message": "Too many requests. Request blocked by rate limiter."
        }

    save_rate_limit(record)

    return {
        "allowed": True,
        "message": "Request allowed"
    }