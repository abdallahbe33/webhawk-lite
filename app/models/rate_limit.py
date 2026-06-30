from datetime import datetime

from app.extensions import db


class RateLimit(db.Model):
    __tablename__ = "rate_limit"

    id = db.Column(db.Integer, primary_key=True)
    backend_id = db.Column(
        db.Integer,
        db.ForeignKey("backend_registration.id"),
        nullable=False
    )
    ip_address = db.Column(db.String(100), nullable=False)
    endpoint = db.Column(db.String(500), nullable=False)
    request_count = db.Column(db.Integer, default=1, nullable=False)
    window_start = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    blocked_until = db.Column(db.DateTime, nullable=True)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False)

    backend = db.relationship("BackendRegistration", back_populates="rate_limits")