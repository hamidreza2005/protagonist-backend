from app.extensions import db
from app.enums.userRole import UserRole
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    
    posts = db.relationship(
        'Post',
        back_populates='author',
        passive_deletes=True
    )

    def toResource(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.value,
        }