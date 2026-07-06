from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Patient(db.Model):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_number: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'document_number': self.document_number,
            'address': self.address,
            'user_id': self.user_id
        }