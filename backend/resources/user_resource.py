from flask import request
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from services.user_service import UserService
from models import Patient, AppointmentStatus
from database import cache



class UserListResource(Resource):
    @auth_token_required
    def get(self):
        return UserService.get_all_users()


class DoctorCreationResource(Resource):
    @auth_token_required
    def post(self):
        data = request.get_json()
        return UserService.create_doctor(data)


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


class PublicDoctorListResource(Resource):
    @auth_token_required
    @cache.cached(timeout=600, key_prefix='public_doctors_list') 
    def get(self):
        """ 
        GET /api/public/doctors 
        Cached for 10 minutes (600s).
        """
        return UserService.get_public_doctors()

class ExportHistoryResource(Resource):
    @auth_token_required
    def post(self):
        """
        Trigger the async CSV export job.
        URL: /api/export/history
        """
        
        from tasks import export_patient_history 
        

        
        export_patient_history.delay(current_user.id, current_user.email)
        
        return {"message": "Export started! You will receive an email shortly."}, 200