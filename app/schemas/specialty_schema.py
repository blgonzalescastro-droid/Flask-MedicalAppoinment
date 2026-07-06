from pydantic import BaseModel

class SpecialtyCreateSchema(BaseModel):
    name: str