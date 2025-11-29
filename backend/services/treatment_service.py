from models import db, Treatment, Appointment, AppointmentStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class TreatmentService:

    @staticmethod
    def add_treatment(appointment_id, diagnosis, prescription, notes, next_visit_date_str=None):
        
        appt = Appointment.query.get(appointment_id)
        if not appt:
            return None, "Appointment ID not found."

        
        if appt.treatment:
            return None, "Treatment details already exist for this appointment. Use PUT to update."

       
        next_visit = None
        if next_visit_date_str:
            try:
                next_visit = datetime.strptime(next_visit_date_str, '%Y-%m-%d').date()
            except ValueError:
                return None, "Invalid date format for next visit. Use YYYY-MM-DD."

        
        new_treatment = Treatment(
            appointment_id=appointment_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes,
            next_visit_suggested=next_visit
        )

        try:
            db.session.add(new_treatment)
            
            
            appt.status = AppointmentStatus.COMPLETED
            
            db.session.commit()
            db.session.refresh(new_treatment)
            return new_treatment, "Treatment added and Appointment marked as Completed."
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_treatment_by_id(t_id):
        return Treatment.query.get(t_id)

    @staticmethod
    def get_treatment_by_appointment(appt_id):
        return Treatment.query.filter_by(appointment_id=appt_id).first()

    @staticmethod
    def update_treatment(t_id, data):
        treatment = Treatment.query.get(t_id)
        if not treatment:
            return None, "Treatment record not found."

        if 'diagnosis' in data: treatment.diagnosis = data['diagnosis']
        if 'prescription' in data: treatment.prescription = data['prescription']
        if 'notes' in data: treatment.notes = data['notes']
        
        if 'next_visit_date' in data:
            try:
                treatment.next_visit_suggested = datetime.strptime(data['next_visit_date'], '%Y-%m-%d').date()
            except ValueError:
                return None, "Invalid date format."

        try:
            db.session.commit()
            db.session.refresh(treatment)
            return treatment, "Treatment updated successfully."
        except Exception as e:
            db.session.rollback()
            return None, str(e)