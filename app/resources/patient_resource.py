from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas.patient_schema import PatientCreateSchema
from app.services.patient_service import PatientService

class PatientListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Listar todos los pacientes
        ---
        tags:
          - Patients
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de pacientes
          500:
            description: Error interno
        """
        try:
            patients = PatientService.get_all_patients()
            return [p.to_json() for p in patients], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def post(self):
        """
        Registrar un paciente asociado a un usuario existente
        ---
        tags:
          - Patients
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [document_number, address, user_id]
              properties:
                document_number:
                  type: string
                  description: DNI de 8 dígitos
                address:
                  type: string
                user_id:
                  type: integer
        responses:
          201:
            description: Paciente creado
          400:
            description: Error de validación, documento duplicado o usuario ya registrado como paciente
          404:
            description: Usuario asociado no existe
        """
        try:
            data = request.get_json()
            validated_data = PatientCreateSchema.model_validate(data)

            result, status_code = PatientService.create_patient(validated_data)
            return result, status_code
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400
