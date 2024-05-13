from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Photo
from app.extensions import db
import os
from werkzeug.utils import secure_filename

bp = Blueprint("photos", __name__)


@bp.route("/search", methods=["GET"])
@login_required
def search_photos():
    keyword = request.args.get("keyword")
    photos = Photo.query.filter(Photo.keywords.like("%{}%".format(keyword))).all()
    results = [
        {
            "image_path": photo.image_path,
            "description": photo.description,
            "keywords": photo.keywords,
        }
        for photo in photos
    ]
    return jsonify(results), 200


@bp.route("/upload", methods=["POST"])
@login_required
def upload_photo():
    file = request.files["file"]
    description = request.form["description"]
    keywords = request.form["keywords"]
    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    file.save(os.path.join("app/static", filepath))
    photo = Photo(
        user_id=current_user.id,
        image_path=filepath,
        description=description,
        keywords=keywords,
    )
    db.session.add(photo)
    db.session.commit()
    return jsonify({"message": "Photo uploaded successfully"}), 201


@bp.route("/photos/<int:photo_id>", methods=["PUT"])
@login_required
def update_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if "description" in request.json:
        photo.description = request.json["description"]
    if "keywords" in request.json:
        photo.keywords = request.json["keywords"]
    db.session.commit()
    return jsonify({"message": "Photo updated successfully"}), 200
