from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas.doctor_schema import DoctorCreateSchema, DoctorUpdateSchema
from app.services.doctor_service import DoctorService

class DoctorListResource(Resource):
    def get(self):
        """
        Listar todos los médicos activos
        ---
        tags:
          - Doctors
        responses:
          200:
            description: Lista de médicos
          500:
            description: Error interno
        """
        try:
            doctors = DoctorService.get_all_doctors()
            return [d.to_json() for d in doctors], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def post(self):
        """
        Crear un médico
        ---
        tags:
          - Doctors
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [name, code, image, speciality_id]
              properties:
                name:
                  type: string
                code:
                  type: string
                  description: Formato "M-XXXXX"
                image:
                  type: string
                speciality_id:
                  type: integer
        responses:
          201:
            description: Médico creado
          400:
            description: Error de validación o código duplicado
        """
        try:
            data = request.get_json()
            validated_data = DoctorCreateSchema.model_validate(data)

            result, status_code = DoctorService.create_doctor(validated_data)
            return result, status_code
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400

class DoctorResource(Resource):
    def get(self, doctor_id):
        """
        Obtener un médico por id
        ---
        tags:
          - Doctors
        parameters:
          - in: path
            name: doctor_id
            type: integer
            required: true
        responses:
          200:
            description: Médico encontrado
          404:
            description: Médico no encontrado
        """
        try:
            doctor = DoctorService.get_by_id(doctor_id)
            if doctor is None:
                return {'error': 'Médico no encontrado'}, 404
            return doctor.to_json(), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def put(self, doctor_id):
        """
        Actualizar un médico
        ---
        tags:
          - Doctors
        security:
          - Bearer: []
        parameters:
          - in: path
            name: doctor_id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [name, image, speciality_id]
              properties:
                name:
                  type: string
                image:
                  type: string
                speciality_id:
                  type: integer
        responses:
          200:
            description: Médico actualizado
          400:
            description: Error de validación
          404:
            description: Médico no encontrado
        """
        try:
            doctor = DoctorService.get_by_id(doctor_id)
            if doctor is None:
                return {'error': 'Médico no encontrado'}, 404

            data = request.get_json()
            validated_data = DoctorUpdateSchema.model_validate(data)

            result, status_code = DoctorService.update_doctor(doctor, validated_data)
            return result, status_code
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, doctor_id):
        """
        Dar de baja (lógica) a un médico
        ---
        tags:
          - Doctors
        security:
          - Bearer: []
        parameters:
          - in: path
            name: doctor_id
            type: integer
            required: true
        responses:
          204:
            description: Médico dado de baja
          404:
            description: Médico no encontrado
        """
        try:
            doctor = DoctorService.get_by_id(doctor_id)
            if doctor is None:
                return {'error': 'Médico no encontrado'}, 404

            DoctorService.delete_doctor(doctor)
            return '', 204
        except Exception as e:
            return {'error': str(e)}, 400
