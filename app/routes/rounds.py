from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models import Round, RoundSession, Scenario

rounds_bp = Blueprint("rounds", __name__)


def round_to_dict(r):
    return {
        "id": str(r.id),
        "session_id": str(r.session.id),
        "scenario_id": str(r.scenario.id),
        "round_number": r.round_number,
        "status": r.status
    }


# Start Round
@rounds_bp.route("/rounds", methods=["POST"])
def start_round():

    data = request.json

    session = RoundSession.objects.get(id=data["session_id"])
    scenario = Scenario.objects.get(id=data["scenario_id"])

    round_obj = Round(
        session=session,
        scenario=scenario,
        round_number=data.get("round_number", 1),
        status="active",
        started_at=datetime.utcnow()
    )

    round_obj.save()

    return jsonify(round_to_dict(round_obj)), 201


# Get Round
@rounds_bp.route("/rounds/<round_id>", methods=["GET"])
def get_round(round_id):

    r = Round.objects(id=round_id).first()

    if not r:
        return {"error": "round not found"}, 404

    return jsonify(round_to_dict(r))


# End Round
@rounds_bp.route("/rounds/<round_id>/end", methods=["POST"])
def end_round(round_id):

    r = Round.objects(id=round_id).first()

    if not r:
        return {"error": "round not found"}, 404

    r.status = "completed"
    r.ended_at = datetime.utcnow()

    r.save()

    return jsonify(round_to_dict(r))
