from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas.specialty_schema import SpecialtyCreateSchema
from app.services.specialty_service import SpecialtyService

class SpecialtyListResource(Resource):
    def get(self):
        """
        Listar todas las especialidades (público)
        ---
        tags:
          - Specialties
        responses:
          200:
            description: Lista de especialidades
          500:
            description: Error interno
        """
        try:
            # Público para que los pacientes busquen especialidades
            specialties = SpecialtyService.get_all_specialties()
            return [s.to_json() for s in specialties], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def post(self):
        """
        Crear una especialidad
        ---
        tags:
          - Specialties
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [name]
              properties:
                name:
                  type: string
        responses:
          201:
            description: Especialidad creada
          400:
            description: Error de validación o especialidad duplicada
        """
        try:
            data = request.get_json()
            validated_data = SpecialtyCreateSchema.model_validate(data)

            result, status_code = SpecialtyService.create_specialty(validated_data)
            return result, status_code
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400
