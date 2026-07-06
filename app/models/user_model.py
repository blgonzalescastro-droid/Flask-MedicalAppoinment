from db import db
from sqlalchemy import Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None, 
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'role_id': self.role_id
        }