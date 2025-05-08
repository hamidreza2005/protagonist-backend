from flask import Blueprint, request, jsonify, current_app
from app.extensions import db, limiter
from app.models.post import Post
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.enums.userRole import UserRole
from sqlalchemy.orm import joinedload

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("", methods=["GET"])
@limiter.limit("60/minute")
def list_posts():
    posts = Post.query.options(joinedload(Post.author)).order_by(Post.created_at.desc()).all()
    return jsonify([
        p.toResource() for p in posts
    ]), 200

@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    p = Post.query.options(joinedload(Post.author)).get_or_404(post_id)
    return jsonify(p.toResource()), 200

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
    return '', 204
