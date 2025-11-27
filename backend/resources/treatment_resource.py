from flask import request
from flask_restful import Resource
from services.treatment_service import TreatmentService

# --- HELPER ---
def treatment_to_dict(t):
    if not t: return {}
    return {
        "id": t.id,
        "appointment_id": t.appointment_id,
        "diagnosis": t.diagnosis,
        "prescription": t.prescription,
        "notes": t.notes,
        "next_visit_suggested": str(t.next_visit_suggested) if t.next_visit_suggested else None,
        # Include Appointment details for context
        "patient_name": t.appointment.patient.user.name if t.appointment.patient else "Unknown",
        "doctor_name": t.appointment.doctor.user.name if t.appointment.doctor else "Unknown"
    }

# --- LIST / CREATE ---
class TreatmentListResource(Resource):
    
    def post(self):
        """ POST /api/treatments """
        data = request.get_json()
        
        # Validation
        if not data.get('appointment_id') or not data.get('diagnosis'):
            return {"message": "Appointment ID and Diagnosis are required."}, 400

        treatment, message = TreatmentService.add_treatment(
            appointment_id=data.get('appointment_id'),
            diagnosis=data.get('diagnosis'),
            prescription=data.get('prescription'),
            notes=data.get('notes'),
            next_visit_date_str=data.get('next_visit_date')
        )

        if not treatment:
            return {"message": message}, 400

        return treatment_to_dict(treatment), 201

# --- SINGLE ITEM ---
class TreatmentResource(Resource):
    
    def get(self, t_id):
        """ GET /api/treatments/<id> """
        treatment = TreatmentService.get_treatment_by_id(t_id)
        if not treatment:
            return {"message": "Treatment not found"}, 404
        return treatment_to_dict(treatment), 200

    def put(self, t_id):
        """ PUT /api/treatments/<id> """
        data = request.get_json()
        treatment, message = TreatmentService.update_treatment(t_id, data)
        
        if not treatment:
            return {"message": message}, 400
        return treatment_to_dict(treatment), 200