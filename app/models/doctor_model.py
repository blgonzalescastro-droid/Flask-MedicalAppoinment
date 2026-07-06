from db import db
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Doctor(db.Model):  # Cambiado a singular
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(7), nullable=False)  # Ejemplo: M-00001 
    image: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    speciality_id: Mapped[int] = mapped_column(ForeignKey('specialties.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'image': self.image,
            'is_active': self.is_active,
            'speciality_id': self.speciality_id
        }