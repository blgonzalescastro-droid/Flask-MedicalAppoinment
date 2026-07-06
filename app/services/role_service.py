from app.models.role_model import Role
from db import db


class RoleService:
    def get_all_roles(self) -> list[Role]:
        return Role.query.all()

    def create_role(self, name: str) -> Role:
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return role


role_service = RoleService()
