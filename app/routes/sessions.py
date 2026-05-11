from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models import RoundSession, User

sessions_bp = Blueprint("sessions", __name__)


def session_to_dict(s):
    return {
        "id": str(s.id),
        "user_id": str(s.user.id),
        "started_at": s.started_at.isoformat(),
        "ended_at": s.ended_at.isoformat() if s.ended_at else None,
        "status": s.status
    }


# Start Session
@sessions_bp.route("/sessions", methods=["POST"])
def start_session():

    data = request.json
    user = User.objects.get(id=data["user_id"])

    session = RoundSession(
        user=user,
        started_at=datetime.utcnow(),
        status="active"
    )

    session.save()

    return jsonify(session_to_dict(session)), 201


# Get Session
@sessions_bp.route("/sessions/<session_id>", methods=["GET"])
def get_session(session_id):

    session = RoundSession.objects(id=session_id).first()

    if not session:
        return {"error": "session not found"}, 404

    return jsonify(session_to_dict(session))


# End Session
@sessions_bp.route("/sessions/<session_id>/end", methods=["POST"])
def end_session(session_id):

    session = RoundSession.objects(id=session_id).first()

    if not session:
        return {"error": "session not found"}, 404

    session.status = "completed"
    session.ended_at = datetime.utcnow()

    session.save()

    return jsonify(session_to_dict(session))
