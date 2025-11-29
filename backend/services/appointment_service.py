from models import db, Appointment, Doctor, Patient, DoctorAvailability, AppointmentStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_security import current_user

class AppointmentService:

    @staticmethod
    def get_all_appointments():
        """
        Returns appointments filtered by the logged-in user's role.
        """
    
        if current_user.has_role('admin'):
            return Appointment.query.all()

       
        elif current_user.has_role('doctor'):
            if not current_user.doctor_profile:
                return [] 
            return Appointment.query.filter_by(doctor_id=current_user.doctor_profile.id).all()

        elif current_user.has_role('patient'):
            if not current_user.patient_profile:
                return []
            return Appointment.query.filter_by(patient_id=current_user.patient_profile.id).all()

        return []

    @staticmethod
    def get_appointment_by_id(appt_id):
        return Appointment.query.get(appt_id)

    @staticmethod
    def book_appointment(patient_user_id, doctor_id, date_str, time_str):

        patient = Patient.query.filter_by(user_id=patient_user_id).first()
        
        if not patient:
            return None, "Patient profile not found. Please contact support."
        
       
        try:
            appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD."

      
        availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, 
            available_date=appt_date
        ).first()

        if not availability:
            return None, "Doctor is not available on this date."
        
        available_slots = availability.available_slots.split(',')
        if time_str not in available_slots:
            return None, f"Doctor is not available at {time_str}."

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

       
        if 'status' in data:
            try:
               
                status_str = data['status']
                if status_str in AppointmentStatus._value2member_map_:
                    appt.status = AppointmentStatus(status_str)
                else:
                    return None, f"Invalid Status: {status_str}"
            except ValueError:
                return None, "Invalid Status."

      
        if 'date' in data:
            try:
                appt.appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return None, "Invalid date format."

     
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

    @staticmethod
    def get_available_slots(doctor_id, date_str):
        """
        Calculates available slots by checking:
        1. Doctor's set schedule
        2. Existing bookings
        3. Past time checks (if today)
        """
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return [], "Invalid date format"

    
        schedule = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, 
            available_date=target_date
        ).first()

        if not schedule:
            return [], "Doctor is not working on this date."

    
        all_slots = [s.strip() for s in schedule.available_slots.split(',') if s.strip()]

      
        booked_appts = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=target_date
        ).filter(Appointment.status != AppointmentStatus.CANCELLED).all()
        
        booked_times = {appt.appointment_time for appt in booked_appts}

     
        final_slots = []
        now = datetime.now()
        is_today = (target_date == now.date())

        for slot in all_slots:
            
            if slot in booked_times:
                continue
            
           
            if is_today:
                try:
                    slot_dt = datetime.strptime(f"{date_str} {slot}", '%Y-%m-%d %H:%M')
                    if slot_dt < now:
                        continue 
                except ValueError:
                    pass 

            final_slots.append(slot)

        return final_slots, None
    
    @staticmethod
    def set_availability(doctor_id, availability_data):
        """
        Saves or Updates availability for a list of dates.
        data format: [{ "date": "2025-11-28", "slots": "09:00,10:00" }, ...]
        """
        try:
            for item in availability_data:
                date_str = item.get('date')
                slots_str = item.get('slots')
                
               
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                
                existing = DoctorAvailability.query.filter_by(
                    doctor_id=doctor_id, 
                    available_date=date_obj
                ).first()

                if existing:
                   
                    existing.available_slots = slots_str
                else:
                    
                    new_avail = DoctorAvailability(
                        doctor_id=doctor_id,
                        available_date=date_obj,
                        available_slots=slots_str
                    )
                    db.session.add(new_avail)
            
            db.session.commit()
            return True, "Availability updated successfully."
        except Exception as e:
            db.session.rollback()
            return False, str(e)