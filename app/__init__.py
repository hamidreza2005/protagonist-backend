from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, migrate, jwt, bcrypt, limiter
from app.controllers.auth import auth_bp
from app.controllers.posts import posts_bp
from app.controllers.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp,   url_prefix="/auth")
    app.register_blueprint(posts_bp,  url_prefix="/posts")
    app.register_blueprint(users_bp,  url_prefix="/users")

    return app
