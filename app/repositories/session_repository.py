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

def deactivate_session(token_hash):
    statement = db.select(UserSession).filter_by(
        token_hash=token_hash
    )

    session = db.session.execute(
        statement
    ).scalar_one_or_none()

    if not session:
        return None

    session.is_active = False
    db.session.commit()

    return session


def list_active_sessions(user_id):
    statement = (
        db.select(UserSession)
        .filter_by(
            user_id=user_id,
            is_active=True,
        )
        .order_by(UserSession.created_at.desc())
    )

    sessions = db.session.execute(
        statement
    ).scalars().all()

    now = datetime.now(timezone.utc)
    active_sessions = []
    changed = False

    for session in sessions:
        expires_at = session.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
                tzinfo=timezone.utc
            )

        if expires_at <= now:
            session.is_active = False
            changed = True
        else:
            active_sessions.append(session)

    if changed:
        db.session.commit()

    return active_sessions
