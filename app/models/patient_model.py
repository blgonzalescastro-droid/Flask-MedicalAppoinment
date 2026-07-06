from db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Patient(db.Model):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    document_number: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)