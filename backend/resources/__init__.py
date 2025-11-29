from resources.auth import auth_bp
from flask import Blueprint
from flask_restful import Api
from resources.appointment_resource import AppointmentListResource, AppointmentResource, DoctorAvailabilityResource,DoctorAvailabilityManageResource
from resources.specialization_resource import SpecializationListResource, SpecializationResource
from resources.treatment_resource import TreatmentListResource, TreatmentResource
from resources.user_resource import UserListResource,UserResource, DoctorCreationResource, PatientHistoryResource,PublicDoctorListResource,ExportHistoryResource
from resources.analytics_resource import AdminAnalyticsResource
from resources.payment_resource import PaymentResource





api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# --- CORRECT MAPPING ---

# 1. For List & Create (POST works here)
api.add_resource(AppointmentListResource, '/appointments') 

# 2. For Single Item (PUT/DELETE works here)
api.add_resource(AppointmentResource, '/appointments/<int:appt_id>')

api.add_resource(SpecializationListResource, '/specializations')
api.add_resource(SpecializationResource, '/specializations/<int:spec_id>')



api.add_resource(TreatmentListResource, '/treatments')
api.add_resource(TreatmentResource, '/treatments/<int:t_id>')

# --- 4. NEW USER & DOCTOR MANAGEMENT ---
# Get all users
api.add_resource(UserListResource, '/users') 

# Create Doctor (Admin only)
api.add_resource(DoctorCreationResource, '/doctors') 

# Get, Update, Delete specific user (Admin or Owner)
api.add_resource(UserResource, '/users/<int:user_id>')

# Patient History (Admin/Doctor view)
api.add_resource(PatientHistoryResource, '/patients/<int:user_id>/history')
api.add_resource(PublicDoctorListResource, '/public/doctors')

api.add_resource(ExportHistoryResource, '/export/history')
api.add_resource(DoctorAvailabilityResource, '/doctors/<int:doctor_id>/slots')
api.add_resource(DoctorAvailabilityManageResource, '/doctor/availability')

api.add_resource(AdminAnalyticsResource, '/admin/analytics')
api.add_resource(PaymentResource, '/pay/<int:appt_id>')

