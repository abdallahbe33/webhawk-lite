from app.extensions import db
from app.models.backend_registration import BackendRegistration
from app.models.security_log import SecurityLog


def create_log(
    backend_id,
    ip_address,
    method,
    endpoint,
    attack_type,
    is_blocked,
    request_data
):
    log = SecurityLog(
        backend_id=backend_id,
        ip_address=ip_address,
        method=method,
        endpoint=endpoint,
        attack_type=attack_type,
        is_blocked=is_blocked,
        request_data=request_data
    )

    db.session.add(log)
    db.session.commit()

    return log


def get_logs_for_user(user_id, blocked_only=False, limit=100):
    query = (
        db.session.query(SecurityLog)
        .join(BackendRegistration)
        .filter(BackendRegistration.user_id == user_id)
    )

    if blocked_only:
        query = query.filter(SecurityLog.is_blocked == True)

    return (
        query
        .order_by(SecurityLog.created_at.desc())
        .limit(limit)
        .all()
    )