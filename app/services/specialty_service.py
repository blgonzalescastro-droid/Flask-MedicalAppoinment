# Servicio con operaciones de especialidades: listado, creación y baja lógica.
from app.models.specialty_model import Specialty
from app.schemas.specialty_schema import SpecialtyCreateSchema
from db import db

class SpecialtyService:
    @staticmethod
    def get_all_specialties() -> list[Specialty]:
        return Specialty.query.filter_by(is_active=True).all()

    @staticmethod
    def get_by_id(id: int) -> Specialty | None:
        return Specialty.query.filter_by(id=id, is_active=True).first()

    @staticmethod
    def find_by_name(name: str) -> Specialty | None:
        return Specialty.query.filter_by(name=name).first()

    @staticmethod
    def create_specialty(data: SpecialtyCreateSchema):
        if SpecialtyService.find_by_name(data.name) is not None:
            return {'error': 'La especialidad ya existe'}, 400

        specialty = Specialty(name=data.name)
        db.session.add(specialty)
        db.session.commit()
        return specialty.to_json(), 201

    @staticmethod
    def update_specialty(specialty: Specialty, data: SpecialtyCreateSchema):
        specialty.name = data.name
        db.session.commit()
        return specialty.to_json(), 200

    @staticmethod
    def delete_specialty(specialty: Specialty):
        specialty.is_active = False
        db.session.commit()

specialty_service = SpecialtyService()
