from pydantic import BaseModel, field_validator

class DoctorCreateSchema(BaseModel):
    name: str
    code: str
    image: str
    speciality_id: int

    @field_validator('code')
    @classmethod
    def validate_doctor_code(cls, v: str) -> str:
        if not v.startswith('M-') or len(v) != 7:
            raise ValueError('El código del médico debe seguir el formato "M-XXXXX" (Ej: M-00001).')
        return v

class DoctorUpdateSchema(BaseModel):
    name: str
    image: str
    speciality_id: int