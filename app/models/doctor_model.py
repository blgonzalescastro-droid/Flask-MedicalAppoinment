from db import db
from sqlalchemy import Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Doctors(db.Model):
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(7), nullable=False) # P-00001
    especialidad: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    def to_json(self):
        
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'especialidad': self.especialidad,
            'image': self.image,
            'is_active': self.is_active,
            'category_id': self.category_id
        }
            