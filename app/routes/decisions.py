from flask import Blueprint, request, jsonify
from datetime import datetime
from mongoengine.errors import DoesNotExist

from ..models import (
    Decision,
    User,
    Scenario,
    Round,
    MetaData,
    MetaParentType
)

decisions_bp = Blueprint("decisions", __name__)


def now():
    return datetime.utcnow()


def decision_to_dict(d):
    return {
        "id": d.id,
        "user_id": d.user.id if d.user else None,
        "scenario_id": d.scenario.id if d.scenario else None,
        "round_id": d.round.id if d.round else None,
        "selected_option": d.selected_option,
        "timestamp": d.timestamp.isoformat() if d.timestamp else None,
    }


# ----------------------------
# Create Decision
# ----------------------------
@decisions_bp.route("/decisions", methods=["POST"])
def create_decision():

    data = request.get_json()

    user_id = data.get("user_id")
    scenario_id = data.get("scenario_id")
    round_id = data.get("round_id")
    selected_option = data.get("selected_option")

    try:
        user = User.objects.get(id=user_id)
        scenario = Scenario.objects.get(id=scenario_id)
        rnd = Round.objects.get(id=round_id)

    except DoesNotExist:
        return jsonify({"error": "Invalid reference"}), 404

    if selected_option >= len(scenario.options):
        return jsonify({"error": "Invalid option"}), 400

    decision = Decision(
        user=user,
        scenario=scenario,
        round=rnd,
        selected_option=selected_option,
        timestamp=now(),
    )

    decision.save()

    return jsonify({
        "decision": decision_to_dict(decision)
    }), 201


# ----------------------------
# Get Decision
# ----------------------------
@decisions_bp.route("/decisions/<decision_id>", methods=["GET"])
def get_decision(decision_id):

    decision = Decision.objects(id=decision_id).first()

    if not decision:
        return jsonify({"error": "Decision not found"}), 404

    return jsonify({
        "decision": decision_to_dict(decision)
    })


# ----------------------------
# List Decisions
# ----------------------------
@decisions_bp.route("/decisions", methods=["GET"])
def list_decisions():

    user_id = request.args.get("user_id")
    round_id = request.args.get("round_id")

    query = Decision.objects

    if user_id:
        query = query.filter(user=user_id)

    if round_id:
        query = query.filter(round=round_id)

    decisions = [decision_to_dict(d) for d in query]

    return jsonify({
        "decisions": decisions
    })


# ----------------------------
# Decisions of Round
# ----------------------------
@decisions_bp.route("/rounds/<round_id>/decisions", methods=["GET"])
def round_decisions(round_id):

    decisions = Decision.objects(round=round_id)

    return jsonify({
        "decisions": [decision_to_dict(d) for d in decisions]
    })


# ----------------------------
# User Strategy Analysis
# ----------------------------
@decisions_bp.route("/users/<user_id>/strategy-analysis", methods=["GET"])
def strategy_analysis(user_id):

    decisions = Decision.objects(user=user_id)

    total = decisions.count()

    if total == 0:
        return jsonify({"strategy": "unknown"})

    coop = decisions.filter(selected_option=0).count()

    coop_rate = coop / total

    if coop_rate > 0.7:
        strategy = "cooperator"
    elif coop_rate < 0.3:
        strategy = "defector"
    else:
        strategy = "mixed"

    return jsonify({
        "strategy": strategy,
        "cooperation_rate": coop_rate
    })


# ----------------------------
# Resolve Decision
# ----------------------------
@decisions_bp.route("/decisions/<decision_id>/resolve", methods=["POST"])
def resolve_decision(decision_id):

    decision = Decision.objects(id=decision_id).first()

    if not decision:
        return jsonify({"error": "Decision not found"}), 404

    opponent_action = 0

    if decision.selected_option == opponent_action:
        payoff = {"player": 2, "opponent": 2}
    else:
        payoff = {"player": 0, "opponent": 3}

    MetaData(
        parent_type=MetaParentType.decision,
        parent_id=decision.id,
        key="resolution",
        value={
            "opponent_action": opponent_action,
            "payoff": payoff
        }
    ).save()

    return jsonify({
        "opponent_action": opponent_action,
        "payoff": payoff
    })
