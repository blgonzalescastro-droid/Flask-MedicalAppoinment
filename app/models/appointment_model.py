from db import db
from sqlalchemy import Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey('doctors.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default='scheduled', nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date.isoformat(), 
            'time': self.time.isoformat() if hasattr(self.time, 'isoformat') else str(self.time),
            'status': self.status
        }