from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from flask_bcrypt import bcrypt
from app.enums.userRole import UserRole

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    password = bcrypt(data['password'])
    user = User(username=data["username"], password=password,role = UserRole.USER)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    hashed_password = bcrypt(data['password'])
    user = User.query.filter_by(username=data["username"]).first()
    if not user or user.password != hashed_password:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
