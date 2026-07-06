from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas.role_schema import RoleCreateSchema
from app.services.role_service import role_service


class RoleListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Listar todos los roles
        ---
        tags:
          - Roles
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de roles
          500:
            description: Error interno
        """
        try:
            roles = role_service.get_all_roles()
            return [r.to_json() for r in roles], 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def post(self):
        """
        Crear un rol
        ---
        tags:
          - Roles
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
            description: Rol creado
          400:
            description: Error de validación
        """
        try:
            data = request.get_json()
            validated_data = RoleCreateSchema.model_validate(data)

            role = role_service.create_role(validated_data.name)
            return role.to_json(), 201
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except Exception as e:
            return {'error': str(e)}, 400
