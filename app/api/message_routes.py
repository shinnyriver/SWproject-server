from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Message, User
from app.extensions import db
from datetime import datetime

bp = Blueprint("messages", __name__, url_prefix="/messages")


@bp.route("/send", methods=["POST"])
@login_required
def send_message():
    receiver_id = request.json["receiver_id"]
    content = request.json["content"]
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow(),
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message sent successfully"}), 201


@bp.route('/<int:other_user_id>', methods=['GET'])
@login_required
def view_messages(other_user_id):
    # 현재 사용자와 선택된 다른 사용자 간의 모든 메시지를 가져옵니다.
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) & (Message.receiver_id == other_user_id) |
        (Message.sender_id == other_user_id) & (Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp).all()

    results = [{
        "id": msg.id,
        "sender_id": msg.sender_id,
        "receiver_id": msg.receiver_id,
        "content": msg.content,
        "timestamp": msg.timestamp.isoformat()
    } for msg in messages]

    return jsonify(results)


@bp.route("/reply/<int:message_id>", methods=["POST"])
@login_required
def reply_message(message_id):
    original_message = Message.query.get_or_404(message_id)
    content = request.json["content"]
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=original_message.sender_id,
        content=content,
        timestamp=datetime.utcnow(),
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Reply sent successfully"}), 201


@bp.route("/delete/<int:message_id>", methods=["DELETE"])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.sender_id == current_user.id or message.receiver_id == current_user.id:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted successfully"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 403
