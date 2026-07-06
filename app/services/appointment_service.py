# Servicio con operaciones de citas médicas: reserva, búsquedas y lógica de negocio.
from app.models.appointment_model import Appointment
from app.schemas.appointment_schema import AppointmentCreateSchema
from db import db

class AppointmentService:
    @staticmethod
    def get_by_id(id: int) -> Appointment | None:
        return Appointment.query.get(id)

    @staticmethod
    def get_appointments_by_user(patient_id: int) -> list[Appointment]:
        return Appointment.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def check_availability(doctor_id: int, date, time) -> Appointment | None:
        # Lógica de negocio para verificar cruce de horarios exactos
        return Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=date,
            time=time,
            status='scheduled'
        ).first()

    @staticmethod
    def create_appointment(patient_id: int, data: AppointmentCreateSchema):
        if AppointmentService.check_availability(data.doctor_id, data.date, data.time) is not None:
            return {'error': 'El médico ya tiene una cita agendada en ese horario'}, 409

        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=data.doctor_id,
            date=data.date,
            time=data.time
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment.to_json(), 201

    @staticmethod
    def cancel_appointment(appointment: Appointment) -> Appointment:
        appointment.status = 'cancelled'
        db.session.commit()
        return appointment

appointment_service = AppointmentService()
