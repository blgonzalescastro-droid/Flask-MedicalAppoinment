from flask import Flask
from db import db
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.models import (
    appointment_model,
    doctor_model,
    patient_model,
    role_model,
    specialty_model,
    user_model
)

from app import router