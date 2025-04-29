from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import jwt_required
from app.decorators.role_required import role_required
from app.enums.userRole import UserRole

users_bp = Blueprint("users", __name__)

@users_bp.route("", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN.value)
def list_users():
    users = User.query.all()
    return jsonify([
        u.toResource()
        for u in users
    ]), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN.value)
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify(u.toResource()), 200

@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(UserRole.ADMIN.value)
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.get_json()
    if "password" in data:
        u.password = bcrypt.generate_password_hash(data["password"]).decode()
    if "role" in data and data["role"] in [r.value for r in UserRole]:
        u.role = UserRole(data["role"])
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required(UserRole.ADMIN.value)
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 204
