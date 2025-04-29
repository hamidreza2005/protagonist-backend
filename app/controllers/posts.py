from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.enums.userRole import UserRole

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("", methods=["GET"])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "created_at": p.created_at.isoformat(),
            "author_id": p.author_id
        } for p in posts
    ]), 200

@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    p = Post.query.get_or_404(post_id)
    return jsonify({
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "created_at": p.created_at.isoformat(),
        "author_id": p.author_id
    }), 200

@posts_bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    author_id = int(get_jwt_identity())
    p = Post(title=data["title"], content=data["content"], author_id=author_id)
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201

@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    p = Post.query.get_or_404(post_id)
    user_id = int(get_jwt_identity())
    claims = getattr(request, "jwt", {})
    role = claims.get("role", "")
    if p.author_id != user_id and role != UserRole.ADMIN.value:
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json()
    p.title = data.get("title", p.title)
    p.content = data.get("content", p.content)
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    p = Post.query.get_or_404(post_id)
    user_id = int(get_jwt_identity())
    claims = getattr(request, "jwt", {})
    role = claims.get("role", "")
    if p.author_id != user_id and role != UserRole.ADMIN.value:
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200
