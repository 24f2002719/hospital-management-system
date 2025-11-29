import uuid  
import random
from datetime import datetime, timedelta
from faker import Faker
from faker_food import FoodProvider
from flask_security.utils import hash_password


from app import app 
from models import (
    db, User, Role, UserRoles, Specialization, Doctor, Patient, 
    Appointment, Treatment, DoctorAvailability, AppointmentStatus
)

fake = Faker()
fake.add_provider(FoodProvider)

def get_or_create_role(name, description):
    """Helper function to find a role or create it if it doesn't exist."""
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name, description=description)
        db.session.add(role)
        print(f" Created Role: {name}")
    else:
        print(f" Role exists: {name}")
    return role

def seed_database():
    with app.app_context():
        

        print("--- Seeding Roles ---")
        admin_role = get_or_create_role('admin', 'Super Administrator') 
        doctor_role = get_or_create_role('doctor', 'Medical Doctor')
        patient_role = get_or_create_role('patient', 'Patient User')
        
        db.session.commit()

        print("--- Seeding Specializations ---")
        specs = [
            "Cardiology", "Dermatology", "Neurology", "Pediatrics", 
            "Orthopedics", "General Surgery", "Psychiatry"
        ]
        specialization_objs = []
        for s_name in specs:
            spec = Specialization.query.filter_by(name=s_name).first()
            if not spec:
                spec = Specialization(name=s_name, description=fake.text(max_nb_chars=50))
                db.session.add(spec)
            specialization_objs.append(spec)
        db.session.commit()

        
        print("--- Skipping Admin User Creation (Already Exists) ---")

        print("--- Seeding Doctors ---")
        current_doc_count = Doctor.query.count()
        if current_doc_count < 10:
            doctor_objs = []
            for i in range(10):
                email = f"doctor{current_doc_count + i}@gmail.com"
                
                if User.query.filter_by(email=email).first(): 
                    continue

                d_user = User(
                    name=fake.name(),
                    email=email,
                    password=hash_password("pass123"), 
                    fs_uniquifier=str(uuid.uuid4()),
                    active=True,
                    address=fake.address(),
                    pincode=fake.postcode()
                )
                db.session.add(d_user)
                db.session.flush()

             
                ur = UserRoles(user_id=d_user.id, role_id=doctor_role.id)
                db.session.add(ur)

                
                spec = random.choice(specialization_objs)
                new_doctor = Doctor(
                    user_id=d_user.id, 
                    specialization_id=spec.id,
                    experience_years=random.randint(2, 25), 
                    bio=fake.paragraph(nb_sentences=3)      
                )
                db.session.add(new_doctor)
                db.session.flush()
                
                doctor_objs.append(new_doctor)
                
             
                for day_offset in range(0, 30, 2):
                    avail_date = datetime.now() + timedelta(days=day_offset)
                    avail = DoctorAvailability(
                        doctor_id=new_doctor.id, 
                        available_date=avail_date.date(),
                        available_slots="09:00,10:00,11:00,14:00,15:00,16:00"
                    )
                    db.session.add(avail)
            
            db.session.commit()
        else:
            print(" Doctors already seeded.")
            doctor_objs = Doctor.query.all()

        print("--- Seeding Patients ---")
        current_pat_count = Patient.query.count()
        if current_pat_count < 50:
            patient_objs = []
            for i in range(50):
                email = f"patient{current_pat_count + i}@gmail.com"
                if User.query.filter_by(email=email).first():
                    continue

                p_user = User(
                    name=fake.name(),
                    email=email,
                    password=hash_password("pass123"),
                    fs_uniquifier=str(uuid.uuid4()),
                    active=True,
                    address=fake.address(),
                    pincode=fake.postcode()
                )
                db.session.add(p_user)
                db.session.flush()

                ur = UserRoles(user_id=p_user.id, role_id=patient_role.id)
                db.session.add(ur)

                new_patient = Patient(user_id=p_user.id, contact_info=fake.phone_number()[:15])
                db.session.add(new_patient)
                patient_objs.append(new_patient)
            db.session.commit()
        else:
            print(" Patients already seeded.")
            patient_objs = Patient.query.all()

        print("--- Seeding Appointments ---")
        if doctor_objs and patient_objs:
            times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
            
            existing_appts = Appointment.query.with_entities(Appointment.doctor_id, Appointment.appointment_date, Appointment.appointment_time).all()
            occupied_slots = set((d_id, date_obj, str(time_str)) for d_id, date_obj, time_str in existing_appts)

            for _ in range(50):
                patient = random.choice(patient_objs)
                doctor = random.choice(doctor_objs)
                
                appt_datetime = fake.date_time_between(start_date='-1y', end_date='+30d')
                appt_date = appt_datetime.date()
                appt_time = random.choice(times)

                slot_key = (doctor.id, appt_date, appt_time)
                if slot_key in occupied_slots:
                    continue
                
                occupied_slots.add(slot_key)

                status = AppointmentStatus.BOOKED
                if appt_date < datetime.now().date():
                    status = AppointmentStatus.COMPLETED
                elif appt_date == datetime.now().date():
                    status = random.choice([AppointmentStatus.BOOKED, AppointmentStatus.CANCELLED])
                
                appt = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    appointment_date=appt_date,
                    appointment_time=appt_time,
                    status=status
                )
                db.session.add(appt)
                db.session.flush()

                if status == AppointmentStatus.COMPLETED:
                    food_item = fake.dish()
                    treatment = Treatment(
                        appointment_id=appt.id,
                        diagnosis=f"Patient consumed too much {food_item}.",
                        prescription=fake.sentence(),
                        notes=fake.text(),
                        next_visit_suggested=appt_date + timedelta(days=14)
                    )
                    db.session.add(treatment)
            
            db.session.commit()
        
        print("--- Database Seeded Successfully! ---")

if __name__ == "__main__":
    seed_database()