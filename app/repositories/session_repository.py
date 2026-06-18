from app.extensions import db
from app.models import UserSession


def create_session(
    user_id,
    token_hash,
    ip_address,
    expires_at,
):
    session = UserSession(
        user_id=user_id,
        token_hash=token_hash,
        ip_address=ip_address,
        expires_at=expires_at,
    )

    db.session.add(session)
    db.session.commit()

    return session