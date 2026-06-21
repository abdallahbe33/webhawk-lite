from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    ip_address = db.Column(
        db.String(45),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    expires_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref="sessions",
    )


def to_dict(self):
    return {
        "id": self.id,
        "ip_address": self.ip_address,
        "created_at": self.created_at.isoformat(),
        "expires_at": self.expires_at.isoformat(),
        "is_active": self.is_active,
    }