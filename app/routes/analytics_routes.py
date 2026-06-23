from flask import Blueprint, g, jsonify

from app.services.analytics_service import (
    get_summary,
    get_attacks_by_type,
    get_recent_attacks
)
from app.utils.auth import jwt_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/analytics/summary")
@jwt_required
def analytics_summary():
    return jsonify(get_summary(g.current_user.id))


@analytics_bp.get("/analytics/attacks-by-type")
@jwt_required
def attacks_by_type():
    return jsonify(
        attacks=get_attacks_by_type(g.current_user.id)
    )


@analytics_bp.get("/analytics/recent-attacks")
@jwt_required
def recent_attacks():
    return jsonify(
        attacks=get_recent_attacks(g.current_user.id)
    )