from db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Role(db.Model):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=True, unique=True)

    def to_json(self):
        
        return {
            'id': self.id,
            'name': self.name
        }