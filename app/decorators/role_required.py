from flask import jsonify, current_app, g
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User
# @app.before_request
def load_user():
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        g.user = User.query.filter_by(id=identity).first()
    except Exception:
        g.user = None

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if g.user == None or g.user.role.value != role:
                return jsonify(msg="Forbidden: Access Denied"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper