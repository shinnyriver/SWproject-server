from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    # 요청에서 JSON 데이터가 없는 경우 에러 메시지 반환
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # 요청 JSON 데이터에서 username과 password 추출
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # username 또는 password가 누락된 경우 에러 메시지 반환
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # 데이터베이스에서 username에 해당하는 사용자 검색
    user = User.query.filter_by(username=username).first()

    # 사용자가 존재하고, 제출된 비밀번호와 해시 비밀번호가 일치하는 경우
    if user and check_password_hash(user.password, password):
        # JWT 토큰 생성
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        # 사용자가 존재하지 않거나 비밀번호가 일치하지 않는 경우
        return jsonify({"msg": "Bad username or password"}), 401