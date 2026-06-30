from app.extensions import db
from app.models.rate_limit import RateLimit


def find_rate_limit(backend_id, ip_address, endpoint):
    return (
        RateLimit.query
        .filter_by(
            backend_id=backend_id,
            ip_address=ip_address,
            endpoint=endpoint
        )
        .first()
    )


def create_rate_limit(backend_id, ip_address, endpoint, window_start):
    record = RateLimit(
        backend_id=backend_id,
        ip_address=ip_address,
        endpoint=endpoint,
        request_count=1,
        window_start=window_start
    )

    db.session.add(record)
    db.session.commit()

    return record


def save_rate_limit(record):
    db.session.commit()
    return record