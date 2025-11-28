from flask import request
from flask_restful import Resource
from flask_security import auth_token_required
from services.user_service import UserService
from models import Patient, AppointmentStatus 

# 1. Resource for Listing Users (GET - Admin)
class UserListResource(Resource):
    @auth_token_required
    def get(self):
        return UserService.get_all_users()

# 2. Resource for Creating Doctors (POST)
class DoctorCreationResource(Resource):
    @auth_token_required
    def post(self):
        data = request.get_json()
        return UserService.create_doctor(data)

# 3. Resource for Single User Operations (GET, PUT, DELETE)
class UserResource(Resource):
    @auth_token_required
    def get(self, user_id):
        return UserService.get_user(user_id)

    @auth_token_required
    def put(self, user_id):
        data = request.get_json()
        return UserService.update_user(user_id, data)

    @auth_token_required
    def delete(self, user_id):
        return UserService.delete_user(user_id)

# 4. Patient History Resource (Updated)
class PatientHistoryResource(Resource):
    @auth_token_required
    def get(self, user_id):
        """
        Fetch completed treatment history for a specific patient.
        URL: /api/patients/<int:user_id>/history
        """
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return {"error": "Patient profile not found"}, 404

        history = []
        for appt in patient.appointments:
            if appt.status == AppointmentStatus.COMPLETED and appt.treatment:
                history.append({
                    "id": appt.id,
                    "date": str(appt.appointment_date),
                    "doctor_name": appt.doctor.user.name,
                    "diagnosis": appt.treatment.diagnosis,
                    "prescription": appt.treatment.prescription,
                    "notes": appt.treatment.notes
                })
        
        history.sort(key=lambda x: x['date'], reverse=True)
        return history, 200

# 5. NEW: Public Doctor List (For Patients)
class PublicDoctorListResource(Resource):
    @auth_token_required
    def get(self):
        """ GET /api/public/doctors """
        return UserService.get_public_doctors()