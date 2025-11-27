from flask import request
from flask_restful import Resource
from flask_security import auth_token_required # <--- Ensure this is imported
from services.appointment_service import AppointmentService

# --- HELPER FUNCTION ---
def to_dict(appt):
    """
    Manually convert the Appointment object to a Dictionary.
    """
    return {
        "id": appt.id,
        "appointment_date": str(appt.appointment_date),  # Changed key to match frontend (appointment_date)
        "appointment_time": appt.appointment_time,
        
        # Status
        "status": appt.status.value if hasattr(appt.status, 'value') else str(appt.status),
        
        # Relationships
        "patient_name": appt.patient.user.name if (appt.patient and appt.patient.user) else "Unknown",
        "doctor_name": appt.doctor.user.name if (appt.doctor and appt.doctor.user) else "Unknown",
        
        # --- NEW FIELDS FOR ADMIN DASHBOARD ---
        "specialization": appt.doctor.specialization.name if (appt.doctor and appt.doctor.specialization) else "General",
        "patient_id_user": appt.patient.user.id if (appt.patient and appt.patient.user) else None, # <--- Needed for History
        # --------------------------------------

        "patient_id": appt.patient_id,
        "doctor_id": appt.doctor_id
    }

# --- LIST RESOURCE ---
class AppointmentListResource(Resource):
    
    @auth_token_required # Recommended to protect this
    def get(self):
        """ GET /api/appointments """
        appointments = AppointmentService.get_all_appointments()
        return [to_dict(a) for a in appointments], 200

    @auth_token_required
    def post(self):
        """ POST /api/appointments """
        data = request.get_json()
        
        appt, message = AppointmentService.book_appointment(
            patient_user_id=data.get('patient_user_id'),
            doctor_id=data.get('doctor_id'),
            date_str=data.get('date'),
            time_str=data.get('time')
        )

        if not appt:
            return {"message": message}, 400
            
        return to_dict(appt), 201

# --- SINGLE ITEM RESOURCE ---
class AppointmentResource(Resource):

    @auth_token_required
    def get(self, appt_id):
        appt = AppointmentService.get_appointment_by_id(appt_id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        return to_dict(appt), 200

    @auth_token_required
    def put(self, appt_id):
        data = request.get_json()
        appt, message = AppointmentService.update_appointment(appt_id, data)
        
        if not appt:
            return {"message": message}, 400
        return to_dict(appt), 200

    @auth_token_required
    def delete(self, appt_id):
        success, message = AppointmentService.delete_appointment(appt_id)
        if success:
            return {"message": message}, 200
        else:
            return {"message": message}, 404