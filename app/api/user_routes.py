from flask import Blueprint, jsonify
from .models import User
from flask_login import login_required, current_user

bp = Blueprint("users", __name__)


@bp.route("/users", methods=["GET"])
def list_users():
    if current_user.is_authenticated:
        users = User.query.all()
        user_data = [{"username": user.username, "id": user.id} for user in users]
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "Unauthorized access"}), 401
