from flask import request
from flask_restful import Resource
from flask_security import auth_token_required 
from services.appointment_service import AppointmentService
from flask_security import current_user
from database import cache

# --- HELPER FUNCTION ---
def to_dict(appt):
    """
    Manually convert the Appointment object to a Dictionary.
    """
    return {
        "id": appt.id,
        "appointment_date": str(appt.appointment_date), 
        "appointment_time": appt.appointment_time,
        
        # Status
        "status": appt.status.value if hasattr(appt.status, 'value') else str(appt.status),
        
        # Relationships
        "patient_name": appt.patient.user.name if (appt.patient and appt.patient.user) else "Unknown",
        "doctor_name": appt.doctor.user.name if (appt.doctor and appt.doctor.user) else "Unknown",
        
        # --- FIELDS FOR DASHBOARDS ---
        "specialization": appt.doctor.specialization.name if (appt.doctor and appt.doctor.specialization) else "General",
        "patient_id_user": appt.patient.user.id if (appt.patient and appt.patient.user) else None,
        
        # IDs
        "patient_id": appt.patient_id,
        "doctor_id": appt.doctor_id
    }

# --- LIST RESOURCE ---
class AppointmentListResource(Resource):
    
    @auth_token_required 
    def get(self):
        """ GET /api/appointments """
        # Get filtered appointments based on role
        appointments = AppointmentService.get_all_appointments()
        
        # Sort by date (Newest first)
        # We use a lambda to handle potential None values gracefully, though DB should enforce non-null
        appointments.sort(key=lambda x: x.appointment_date, reverse=True)
        
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
        
class DoctorAvailabilityResource(Resource):
    
    # We use make_cache_key to create unique keys per doctor + date
    # key will look like: "hms_slots_doctor_5_date_2025-11-28"
    def _make_cache_key(self):
        doctor_id = request.view_args['doctor_id']
        date_str = request.args.get('date')
        return f"slots_doctor_{doctor_id}_date_{date_str}"

    @auth_token_required
    @cache.cached(timeout=60, key_prefix=_make_cache_key) # <--- Dynamic Cache Key
    def get(self, doctor_id):
        """
        GET /api/doctors/<int:doctor_id>/slots?date=YYYY-MM-DD
        Cached for 60 seconds to reduce DB load.
        """
        date_str = request.args.get('date')
        if not date_str:
            return {"message": "Date parameter is required"}, 400
            
        slots, error = AppointmentService.get_available_slots(doctor_id, date_str)
        
        if error:
            return {"slots": [], "message": error}, 200
            
        return {"slots": slots}, 200
    
class DoctorAvailabilityManageResource(Resource):
    @auth_token_required
    def post(self):
        """
        POST /api/doctor/availability
        Body: [ { "date": "2025-11-28", "slots": "09:00,10:00" }, ... ]
        """
        # Security Check
        if not current_user.has_role('doctor') or not current_user.doctor_profile:
            return {"message": "Unauthorized. Only doctors can set availability."}, 403

        data = request.get_json() # Expecting a list
        
        success, message = AppointmentService.set_availability(
            doctor_id=current_user.doctor_profile.id,
            availability_data=data
        )
        
        if success:
            return {"message": message}, 200
        return {"message": message}, 400