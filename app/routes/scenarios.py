from flask import Blueprint, request, jsonify
from mongoengine.errors import DoesNotExist, ValidationError

from ..models import Scenario, Category

scenarios_bp = Blueprint("scenarios", __name__)


def scenario_to_dict(s):
    return {
        "id": s.id,
        "text": s.text,
        "options": s.options,
        "correct_option": s.correct_option,
        "category_id": s.category.id if s.category else None,
        "category_name": s.category.name if s.category else None,
        "created_at": s.created_at.isoformat() if getattr(s, "created_at", None) else None,
        "updated_at": s.updated_at.isoformat() if getattr(s, "updated_at", None) else None,
    }


# ----------------------------
# Create Scenario
# ----------------------------
@scenarios_bp.route("/scenarios", methods=["POST"])
def create_scenario():
    data = request.get_json(silent=True) or {}

    text = data.get("text")
    options = data.get("options", [])
    correct_option = data.get("correct_option")
    category_id = data.get("category_id")

    if not text:
        return jsonify({"error": "text is required"}), 400

    if not isinstance(options, list) or len(options) < 2:
        return jsonify({"error": "options must be a list with at least 2 items"}), 400

    if not isinstance(correct_option, int):
        return jsonify({"error": "correct_option must be an integer"}), 400

    if correct_option < 0 or correct_option >= len(options):
        return jsonify({"error": "correct_option is out of range"}), 400

    category = None
    if category_id:
        category = Category.objects(id=category_id).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404

    try:
        scenario = Scenario(
            text=text,
            options=options,
            correct_option=correct_option,
            category=category
        )
        scenario.save()
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": str(e)}), 400

    return jsonify({
        "message": "Scenario created successfully",
        "scenario": scenario_to_dict(scenario)
    }), 201


# ----------------------------
# Get Scenario by ID
# ----------------------------
@scenarios_bp.route("/scenarios/<scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    scenario = Scenario.objects(id=scenario_id).first()

    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404

    return jsonify({
        "scenario": scenario_to_dict(scenario)
    }), 200


# ----------------------------
# List Scenarios
# ----------------------------
@scenarios_bp.route("/scenarios", methods=["GET"])
def list_scenarios():
    category_id = request.args.get("category_id")
    text_query = request.args.get("q")
    limit = request.args.get("limit", 50, type=int)
    skip = request.args.get("skip", 0, type=int)

    query = Scenario.objects

    if category_id:
        query = query.filter(category=category_id)

    if text_query:
        query = query.filter(text__icontains=text_query)

    total = query.count()
    scenarios = query.skip(skip).limit(limit)

    return jsonify({
        "total": total,
        "skip": skip,
        "limit": limit,
        "scenarios": [scenario_to_dict(s) for s in scenarios]
    }), 200


# ----------------------------
# Update Scenario
# ----------------------------
@scenarios_bp.route("/scenarios/<scenario_id>", methods=["PUT"])
def update_scenario(scenario_id):
    scenario = Scenario.objects(id=scenario_id).first()

    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404

    data = request.get_json(silent=True) or {}

    text = data.get("text", scenario.text)
    options = data.get("options", scenario.options)
    correct_option = data.get("correct_option", scenario.correct_option)
    category_id = data.get("category_id")

    if not text:
        return jsonify({"error": "text cannot be empty"}), 400

    if not isinstance(options, list) or len(options) < 2:
        return jsonify({"error": "options must be a list with at least 2 items"}), 400

    if not isinstance(correct_option, int):
        return jsonify({"error": "correct_option must be an integer"}), 400

    if correct_option < 0 or correct_option >= len(options):
        return jsonify({"error": "correct_option is out of range"}), 400

    if category_id is not None:
        if category_id == "":
            scenario.category = None
        else:
            category = Category.objects(id=category_id).first()
            if not category:
                return jsonify({"error": "Category not found"}), 404
            scenario.category = category

    scenario.text = text
    scenario.options = options
    scenario.correct_option = correct_option

    try:
        scenario.save()
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": str(e)}), 400

    return jsonify({
        "message": "Scenario updated successfully",
        "scenario": scenario_to_dict(scenario)
    }), 200


# ----------------------------
# Delete Scenario
# ----------------------------
@scenarios_bp.route("/scenarios/<scenario_id>", methods=["DELETE"])
def delete_scenario(scenario_id):
    scenario = Scenario.objects(id=scenario_id).first()

    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404

    scenario.delete()

    return jsonify({
        "message": "Scenario deleted successfully",
        "scenario_id": scenario_id
    }), 200


# ----------------------------
# Get Scenarios by Category
# ----------------------------
@scenarios_bp.route("/categories/<category_id>/scenarios", methods=["GET"])
def get_category_scenarios(category_id):
    category = Category.objects(id=category_id).first()
    if not category:
        return jsonify({"error": "Category not found"}), 404

    scenarios = Scenario.objects(category=category)

    return jsonify({
        "category_id": category.id,
        "category_name": category.name,
        "scenarios": [scenario_to_dict(s) for s in scenarios]
    }), 200


# ----------------------------
# Get Random Scenario
# ----------------------------
@scenarios_bp.route("/scenarios/random", methods=["GET"])
def get_random_scenario():
    category_id = request.args.get("category_id")

    query = Scenario.objects
    if category_id:
        query = query.filter(category=category_id)

    scenario = query.order_by("?").first()

    if not scenario:
        return jsonify({"error": "No scenario found"}), 404

    return jsonify({
        "scenario": scenario_to_dict(scenario)
    }), 200


# ----------------------------
# Validate Answer
# ----------------------------
@scenarios_bp.route("/scenarios/<scenario_id>/validate-answer", methods=["POST"])
def validate_answer(scenario_id):
    scenario = Scenario.objects(id=scenario_id).first()

    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404

    data = request.get_json(silent=True) or {}
    selected_option = data.get("selected_option")

    if not isinstance(selected_option, int):
        return jsonify({"error": "selected_option must be an integer"}), 400

    if selected_option < 0 or selected_option >= len(scenario.options):
        return jsonify({"error": "selected_option is out of range"}), 400

    is_correct = selected_option == scenario.correct_option

    return jsonify({
        "scenario_id": scenario.id,
        "selected_option": selected_option,
        "correct_option": scenario.correct_option,
        "is_correct": is_correct
    }), 200
