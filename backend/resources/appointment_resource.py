from flask import request
from flask_restful import Resource
from flask_security import auth_token_required 
from services.appointment_service import AppointmentService
from database import cache 

def to_dict(appt):
    return {
        "id": appt.id,
        "appointment_date": str(appt.appointment_date),
        "appointment_time": appt.appointment_time,
        "status": appt.status.value if hasattr(appt.status, 'value') else str(appt.status),
        "patient_name": appt.patient.user.name if (appt.patient and appt.patient.user) else "Unknown",
        "doctor_name": appt.doctor.user.name if (appt.doctor and appt.doctor.user) else "Unknown",
        "specialization": appt.doctor.specialization.name if (appt.doctor and appt.doctor.specialization) else "General",
        "patient_id_user": appt.patient.user.id if (appt.patient and appt.patient.user) else None,
        "patient_id": appt.patient_id,
        "doctor_id": appt.doctor_id,
        
      
        "is_paid": getattr(appt, 'is_paid', False), 
        "amount": getattr(appt, 'amount', 500)      
  
    }

def make_availability_cache_key():
    """Generates a unique key based on doctor ID and Date"""

    doctor_id = request.view_args.get('doctor_id')
    date_str = request.args.get('date')
    return f"slots_doc_{doctor_id}_date_{date_str}"


class AppointmentListResource(Resource):
    
    @auth_token_required 
    def get(self):
        """ GET /api/appointments """
        appointments = AppointmentService.get_all_appointments()
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
    
    @auth_token_required
    
    @cache.cached(timeout=60, key_prefix=make_availability_cache_key) 
    def get(self, doctor_id):
        """
        GET /api/doctors/<int:doctor_id>/slots?date=YYYY-MM-DD
        Cached for 60 seconds.
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
        from flask_security import current_user
        if not current_user.has_role('doctor') or not current_user.doctor_profile:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        
        success, message = AppointmentService.set_availability(
            doctor_id=current_user.doctor_profile.id,
            availability_data=data
        )
        
      
        if success:
            return {"message": message}, 200
        return {"message": message}, 400