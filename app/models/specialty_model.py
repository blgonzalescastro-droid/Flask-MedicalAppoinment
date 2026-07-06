from db import db
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Specialty(db.Model):
    __tablename__ = 'specialties'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_json(self):
        
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active
        }