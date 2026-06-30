from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class BackendRegistration(db.Model):
    __tablename__ = "backend_registration"

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

    service_name = db.Column(
        db.String(150),
        nullable=False,
    )

    target_url = db.Column(
        db.String(2048),
        nullable=False,
    )

    api_key = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref="backends",
    )
    security_logs = db.relationship(
    "SecurityLog",
    back_populates="backend",
    cascade="all, delete-orphan"
    ) 

    rate_limits = db.relationship(
    "RateLimit",
    back_populates="backend",
    cascade="all, delete-orphan"
    )   
    def to_dict(self):
        return {
            "id": self.id,
            "service_name": self.service_name,
            "target_url": self.target_url,
            "api_key": self.api_key,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    