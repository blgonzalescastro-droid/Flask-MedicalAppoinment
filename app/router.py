from flask_restful import Api
from app import app
from app.resources.auth_resource import LoginResource, RegisterResource
from app.resources.patient_resource import PatientListResource
from app.resources.specialty_resource import SpecialtyListResource
from app.resources.doctor_resource import DoctorListResource, DoctorResource
from app.resources.appointment_resource import AppointmentResource, UserAppointmentListResource
from app.resources.role_resource import RoleListResource

api = Api(app, prefix='/api/v1')

api.add_resource(LoginResource, '/auth/login')
api.add_resource(RegisterResource, '/auth/register')

api.add_resource(RoleListResource, '/roles')
api.add_resource(PatientListResource, '/patients')

api.add_resource(SpecialtyListResource, '/specialties')

api.add_resource(DoctorListResource, '/doctors')
api.add_resource(DoctorResource, '/doctors/<int:doctor_id>')

api.add_resource(AppointmentResource, '/appointments')
api.add_resource(UserAppointmentListResource, '/appointments/my-appointments')