from app.extensions import db
from app.models import UserSession
from datetime import datetime, timezone


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
def find_active_session(token_hash):
    statement = db.select(UserSession).filter_by(
        token_hash=token_hash,
        is_active=True,
    )

    session = db.session.execute(
        statement
    ).scalar_one_or_none()

    if not session:
        return None

    expires_at = session.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at <= datetime.now(timezone.utc):
        session.is_active = False
        db.session.commit()

        return None

    return session
