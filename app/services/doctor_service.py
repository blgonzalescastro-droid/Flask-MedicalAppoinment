
from app.models.doctor_model import Doctor
from app.schemas.doctor_schema import DoctorCreateSchema, DoctorUpdateSchema
from db import db

class DoctorService:
    @staticmethod
    def get_all_doctors() -> list[Doctor]:
        return Doctor.query.filter_by(is_active=True).all()

    @staticmethod
    def get_by_id(id: int) -> Doctor | None:
        return Doctor.query.filter_by(id=id, is_active=True).first()

    @staticmethod
    def find_by_code(code: str) -> Doctor | None:
        return Doctor.query.filter_by(code=code).first()

    @staticmethod
    def create_doctor(data: DoctorCreateSchema):
        if DoctorService.find_by_code(data.code) is not None:
            return {'error': 'El código de médico ya existe'}, 400

        doctor = Doctor(
            name=data.name,
            code=data.code,
            image=data.image,
            speciality_id=data.speciality_id
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor.to_json(), 201

    @staticmethod
    def update_doctor(doctor: Doctor, data: DoctorUpdateSchema):
        # El código no se edita por ser el identificador de colegiatura
        doctor.name = data.name
        doctor.image = data.image
        doctor.speciality_id = data.speciality_id
        db.session.commit()
        return doctor.to_json(), 200

    @staticmethod
    def delete_doctor(doctor: Doctor):
        doctor.is_active = False
        db.session.commit()

doctor_service = DoctorService()
