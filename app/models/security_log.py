from datetime import datetime

from app.extensions import db


class SecurityLog(db.Model):
    __tablename__ = "security_logs"

    id = db.Column(db.Integer, primary_key=True)
    backend_id = db.Column(
        db.Integer,
        db.ForeignKey("backend_registration.id"),
        nullable=True
    )
    ip_address = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(20), nullable=False)
    endpoint = db.Column(db.String(500), nullable=False)
    attack_type = db.Column(db.String(100), nullable=True)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False)
    request_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    backend = db.relationship("BackendRegistration", back_populates="security_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "backend_id": self.backend_id,
            "ip_address": self.ip_address,
            "method": self.method,
            "endpoint": self.endpoint,
            "attack_type": self.attack_type,
            "is_blocked": self.is_blocked,
            "request_data": self.request_data,
            "created_at": self.created_at.isoformat()
        }