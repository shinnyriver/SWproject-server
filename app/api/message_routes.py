from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Message, User
from app.extensions import db
from datetime import datetime

bp = Blueprint("messages", __name__)


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


@bp.route("/inbox", methods=["GET"])
@login_required
def view_messages():
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    results = [
        {
            "sender": User.query.get(msg.sender_id).username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in messages
    ]
    return jsonify(results), 200


@bp.route("/reply_message/<int:message_id>", methods=["POST"])
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


@bp.route("/delete_message/<int:message_id>", methods=["DELETE"])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.sender_id == current_user.id or message.receiver_id == current_user.id:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted successfully"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 403
