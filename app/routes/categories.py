from flask import Blueprint, request, jsonify
from ..models import Category, EconomyFunction

categories_bp = Blueprint("categories", __name__)


def category_to_dict(c):
    return {
        "id": str(c.id),
        "name": c.name,
        "description": c.description,
        "functions": [str(f.id) for f in c.function_pipeline]
    }


# Create Category
@categories_bp.route("/categories", methods=["POST"])
def create_category():

    data = request.json

    name = data.get("name")
    description = data.get("description")
    function_ids = data.get("function_ids", [])

    functions = EconomyFunction.objects(id__in=function_ids)

    category = Category(
        name=name,
        description=description,
        function_pipeline=list(functions)
    )

    category.save()

    return jsonify(category_to_dict(category)), 201


# List Categories
@categories_bp.route("/categories", methods=["GET"])
def list_categories():

    categories = Category.objects()

    return jsonify([category_to_dict(c) for c in categories])


# Get Category
@categories_bp.route("/categories/<category_id>", methods=["GET"])
def get_category(category_id):

    category = Category.objects(id=category_id).first()

    if not category:
        return {"error": "category not found"}, 404

    return jsonify(category_to_dict(category))


# Update Category
@categories_bp.route("/categories/<category_id>", methods=["PUT"])
def update_category(category_id):

    category = Category.objects(id=category_id).first()

    if not category:
        return {"error": "category not found"}, 404

    data = request.json

    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)

    category.save()

    return jsonify(category_to_dict(category))


# Delete Category
@categories_bp.route("/categories/<category_id>", methods=["DELETE"])
def delete_category(category_id):

    category = Category.objects(id=category_id).first()

    if not category:
        return {"error": "category not found"}, 404

    category.delete()

    return {"message": "category deleted"}
