
from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.models.user_model import User
from db import db
from app.utils.helpers import hash_password, verify_password, CryptoHelper
from app.services.user_service import user_service
from flask_jwt_extended import create_access_token, create_refresh_token

class LoginResource(Resource):
    def post(self):
        """
        Iniciar sesión y obtener tokens JWT
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
        responses:
          200:
            description: Tokens de acceso y refresco
            schema:
              type: object
              properties:
                access:
                  type: string
                refresh:
                  type: string
          400:
            description: Error de validación
          401:
            description: Usuario no encontrado o contraseña incorrecta
        """
        try:
            data = request.get_json()
            validated_data = LoginSchema.model_validate(data)

            user = user_service.find_by_email(validated_data.email)

            if user is None:
                return {
                    'error': 'User not found'
                }, 401
            
            is_pwd_valid = verify_password(user.password, validated_data.password)

            if not is_pwd_valid:
                return {
                    'error': 'Password incorrect'
                }, 401
            
            crypto = CryptoHelper()
            hashed_id = crypto.encrypt(user.id)
            
            access_token = create_access_token(
                identity=hashed_id,
                additional_claims={
                    'name': user.name,
                    'last_name': user.last_name,
                    'email': user.email
                }
            )
            refresh_token = create_refresh_token(
                identity=hashed_id
            )

            return {
                'access': access_token,
                'refresh': refresh_token
            }, 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class RegisterResource(Resource):
    def post(self):
        """
        Registrar un nuevo usuario
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [name, last_name, email, password, role_id]
              properties:
                name:
                  type: string
                last_name:
                  type: string
                email:
                  type: string
                  format: email
                password:
                  type: string
                role_id:
                  type: integer
        responses:
          200:
            description: Usuario creado
          400:
            description: Error de validación o email ya registrado
        """
        try:
            data = request.get_json()
            validated_data = RegisterSchema.model_validate(data)

            user = user_service.find_by_email(validated_data.email)

            if user is not None:
                return {
                    'error': 'Email already exists'
                }, 400

            created_user = User(
                name=validated_data.name,
                last_name=validated_data.last_name,
                email=validated_data.email,
                password=hash_password(validated_data.password),
                role_id=validated_data.role_id
            )

            db.session.add(created_user)
            db.session.commit()

            return created_user.to_json(), 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400