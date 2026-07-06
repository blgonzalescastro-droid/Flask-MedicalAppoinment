from pydantic import BaseModel, field_validator

class PatientCreateSchema(BaseModel):
    document_number: str
    address: str
    user_id: int

    @field_validator('document_number')
    @classmethod
    def validate_dni_length(cls, v: str) -> str:
        if len(v) != 8 or not v.isdigit():
            raise ValueError('El número de documento debe tener exactamente 8 dígitos numéricos.')
        return v