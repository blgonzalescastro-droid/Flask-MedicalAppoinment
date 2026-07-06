from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.appointment_schema import AppointmentCreateSchema
from app.services.appointment_service import AppointmentService
from app.utils.helpers import CryptoHelper

class AppointmentResource(Resource):
    @jwt_required()
    def post(self):
        """
        Reservar una cita médica
        ---
        tags:
          - Appointments
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [doctor_id, date, time]
              properties:
                doctor_id:
                  type: integer
                date:
                  type: string
                  format: date
                time:
                  type: string
                  format: time
        responses:
          201:
            description: Cita creada
          400:
            description: Error de validación
          409:
            description: El médico ya tiene una cita agendada en ese horario
        """
        try:
            # 1. Obtener la identidad cifrada desde el JWT y desencriptarla
            hashed_id = get_jwt_identity()
            crypto = CryptoHelper()
            user_id = crypto.decrypt(hashed_id) # Convierte el hash de vuelta al ID entero de la BD

            # 2. Validar el cuerpo del JSON enviado por el cliente
            data = request.get_json()
            validated_data = AppointmentCreateSchema.model_validate(data)

            # 3. Delegar la lógica de negocio al servicio de turnos
            result, status_code = AppointmentService.create_appointment(user_id, validated_data)
            return result, status_code

        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400

class UserAppointmentListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Listar las citas del usuario autenticado
        ---
        tags:
          - Appointments
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de citas del usuario
          500:
            description: Error interno
        """
        try:
            hashed_id = get_jwt_identity()
            crypto = CryptoHelper()
            user_id = crypto.decrypt(hashed_id)

            appointments = AppointmentService.get_appointments_by_user(user_id)
            return [a.to_json() for a in appointments], 200
        except Exception as e:
            return {'error': str(e)}, 500
