from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.extensions import db

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201
