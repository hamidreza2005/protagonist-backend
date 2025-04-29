from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db, bcrypt, limiter
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from app.enums.userRole import UserRole
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5/minute")
def register():
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data["username"], password=password, role=UserRole.USER)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5/minute")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    remember = data.get("remember", False)
    expires = timedelta(days=30 if remember else 1)
    additional_claims = {"role": user.role.value}

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
        expires_delta=expires
    )

    response = jsonify({
        "message": "Login successful",
        "data": {
            "token" : access_token,
            "expires": expires.total_seconds()
        }
    })

    return response

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def identify_me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role.value
    }), 200
