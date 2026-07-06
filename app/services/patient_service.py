# Servicio con operaciones de pacientes: búsqueda, creación y listados.
from app.models.patient_model import Patient
from app.models.user_model import User
from app.schemas.patient_schema import PatientCreateSchema
from db import db

class PatientService:
    @staticmethod
    def get_all_patients() -> list[Patient]:
        return Patient.query.all()

    @staticmethod
    def get_by_id(id: int) -> Patient | None:
        return Patient.query.get(id)

    @staticmethod
    def find_by_user_id(user_id: int) -> Patient | None:
        return Patient.query.filter_by(user_id=user_id).first()

    @staticmethod
    def find_by_document(document_number: str) -> Patient | None:
        return Patient.query.filter_by(document_number=document_number).first()

    @staticmethod
    def create_patient(data: PatientCreateSchema):
        user = User.query.filter_by(id=data.user_id, is_active=True).first()
        if user is None:
            return {'error': 'El usuario asociado no existe'}, 404

        if PatientService.find_by_user_id(data.user_id) is not None:
            return {'error': 'Este usuario ya tiene un paciente registrado'}, 400

        if PatientService.find_by_document(data.document_number) is not None:
            return {'error': 'El número de documento ya está registrado'}, 400

        patient = Patient(
            name=user.name,
            last_name=user.last_name,
            document_number=data.document_number,
            address=data.address,
            user_id=data.user_id
        )
        db.session.add(patient)
        db.session.commit()
        return patient.to_json(), 201

patient_service = PatientService()
