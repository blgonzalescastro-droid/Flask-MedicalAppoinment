from db import db
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String(255), nullable=False)
    time: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_json(self):
        
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'time': self.time
        }