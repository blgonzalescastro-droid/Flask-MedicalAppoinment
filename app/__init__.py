from flask import Flask
from db import db
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
app.config['SWAGGER'] = {
    'title': 'Medical Appointment API',
    'uiversion': 3,
    'specs_route': '/apidocs/'
}
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
swagger = Swagger(app, template={
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT como: **Bearer &lt;token&gt;**'
        }
    }
})

from app.models import (
    appointment_model,
    doctor_model,
    patient_model,
    role_model,
    specialty_model,
    user_model
)

from app import router