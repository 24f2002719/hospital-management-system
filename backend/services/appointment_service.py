from models import db, Appointment, Doctor, Patient, DoctorAvailability, AppointmentStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_security import current_user  # <--- Import this

class AppointmentService:

    @staticmethod
    def get_all_appointments():
        """
        Returns appointments filtered by the logged-in user's role.
        """
        # 1. Admin: See EVERYTHING
        if current_user.has_role('admin'):
            return Appointment.query.all()

        # 2. Doctor: See ONLY their own appointments
        elif current_user.has_role('doctor'):
            # Safety check: Ensure the user actually has a doctor profile
            if not current_user.doctor_profile:
                return [] 
            return Appointment.query.filter_by(doctor_id=current_user.doctor_profile.id).all()

        # 3. Patient: See ONLY their own appointments
        elif current_user.has_role('patient'):
            # Safety check
            if not current_user.patient_profile:
                return []
            return Appointment.query.filter_by(patient_id=current_user.patient_profile.id).all()

        # Default: Return empty list if no role matches
        return []

    @staticmethod
    def get_appointment_by_id(appt_id):
        return Appointment.query.get(appt_id)

    @staticmethod
    def book_appointment(patient_user_id, doctor_id, date_str, time_str):
        # 1. Find Patient
        patient = Patient.query.filter_by(user_id=patient_user_id).first()
        
        if not patient:
            # --- DEBUGGING BLOCK START ---
            print("❌ NOT FOUND! Printing all valid Patient User IDs in this database:")
            all_patients = Patient.query.all()
            valid_ids = [p.user_id for p in all_patients]
            print(f"👉 VALID USER IDs: {valid_ids}")
            
            print(f"📂 Database File being used: {db.engine.url}")
            print("-" * 30)
            # --- DEBUGGING BLOCK END ---
            
            return None, f"Patient profile not found. Valid User IDs are: {valid_ids}"
        
        # 2. Parse Date
        try:
            appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD."

        # 3. Check Availability
        availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, 
            available_date=appt_date
        ).first()

        if not availability:
            return None, "Doctor is not available on this date."
        
        available_slots = availability.available_slots.split(',')
        if time_str not in available_slots:
            return None, f"Doctor is not available at {time_str}."

        # 4. Create Object
        new_appt = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=appt_date,
            appointment_time=time_str,
            status=AppointmentStatus.BOOKED
        )

        try:
            db.session.add(new_appt)
            db.session.commit()
            
            db.session.refresh(new_appt)
            
            return new_appt, "Appointment booked successfully."
        except IntegrityError:
            db.session.rollback()
            return None, "Slot already booked (Double Booking)."
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_appointment(appt_id, data):
        appt = Appointment.query.get(appt_id)
        if not appt:
            return None, "Appointment not found"

        # Update Status
        if 'status' in data:
            try:
                # Handle Enum conversion safely
                status_str = data['status']
                # If the string matches the Enum value (e.g. 'Booked')
                if status_str in AppointmentStatus._value2member_map_:
                    appt.status = AppointmentStatus(status_str)
                else:
                    return None, f"Invalid Status: {status_str}"
            except ValueError:
                return None, "Invalid Status."

        # Update Date
        if 'date' in data:
            try:
                appt.appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return None, "Invalid date format."

        # Update Time
        if 'time' in data:
            appt.appointment_time = data['time']

        try:
            db.session.commit()
            db.session.refresh(appt)
            return appt, "Appointment updated successfully."
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_appointment(appt_id):
        appt = Appointment.query.get(appt_id)
        if not appt:
            return False, "Appointment not found"
        
        try:
            db.session.delete(appt)
            db.session.commit()
            return True, "Deleted"
        except Exception as e:
            return False, str(e)