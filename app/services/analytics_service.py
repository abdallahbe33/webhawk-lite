from sqlalchemy import func

from app.extensions import db
from app.models.backend_registration import BackendRegistration
from app.models.security_log import SecurityLog


def get_summary(user_id):
    base_query = (
        db.session.query(SecurityLog)
        .join(BackendRegistration)
        .filter(BackendRegistration.user_id == user_id)
    )

    total_requests = base_query.count()
    blocked_requests = base_query.filter(SecurityLog.is_blocked == True).count()
    allowed_requests = total_requests - blocked_requests

    return {
        "total_scanned_requests": total_requests,
        "total_blocked_requests": blocked_requests,
        "total_allowed_requests": allowed_requests
    }


def get_attacks_by_type(user_id):
    rows = (
        db.session.query(
            SecurityLog.attack_type,
            func.count(SecurityLog.id)
        )
        .join(BackendRegistration)
        .filter(
            BackendRegistration.user_id == user_id,
            SecurityLog.is_blocked == True
        )
        .group_by(SecurityLog.attack_type)
        .all()
    )

    return [
        {
            "attack_type": attack_type,
            "count": count
        }
        for attack_type, count in rows
    ]


def get_recent_attacks(user_id, limit=10):
    attacks = (
        db.session.query(SecurityLog)
        .join(BackendRegistration)
        .filter(
            BackendRegistration.user_id == user_id,
            SecurityLog.is_blocked == True
        )
        .order_by(SecurityLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return [attack.to_dict() for attack in attacks]