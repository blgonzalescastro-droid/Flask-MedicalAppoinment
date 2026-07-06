# Servicio con operaciones de usuarios: búsqueda, creación y validación.
from app.models.user_model import User
from app.schemas.auth_schema import RegisterSchema
from db import db

class UserService:
    def get_all(self) -> list[User]:
        return User.query.filter_by(is_active=True).all()

    def find_by_email(self, email: str) -> User | None:
        user = User.query.filter_by(
            email=email, 
            is_active=True
        ).first()
        return user

    def get_by_id(self, id: int) -> User | None:
        user = User.query.filter_by(
            id=id, 
            is_active=True
        ).first()
        return user

    def create(self, data: RegisterSchema, password_hash: str) -> User:
        user = User(
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            password=password_hash,
            role_id=data.role_id
        )
        db.session.add(user)
        db.session.commit()
        return user

user_service = UserService()