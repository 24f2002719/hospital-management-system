from app import app 
from database import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password


# Run like this in backend folder  - python -m backend.scripts.init_db

with app.app_context():

    db.drop_all()
    db.create_all()

    datastore : SQLAlchemyUserDatastore  = app.datastore

    # Use consistent lowercase names so lookups match
    admin_role  = datastore.find_or_create_role("admin",  description="Super User")
    doctor_role = datastore.find_or_create_role("doctor", description="Doctor Role")
    patient_role= datastore.find_or_create_role("patient",description="Patient Role")

    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(
            email = "admin@gmail.com",
            name = "admin",
            password = hash_password("admin123")
        )

    if not datastore.find_user(email="doctor@gmail.com"):
        datastore.create_user(
            email = "doctor@gmail.com",
            name = "doctor",
            password = hash_password("doctor123")
        )
    
    if not datastore.find_user(email="patient@gmail.com"):
        datastore.create_user(
            email = "patient@gmail.com",
            name = "patient",
            password = hash_password("patient123")
        )

    try:
        db.session.commit()
        print("Data Set Created")
    except Exception as e:
        db.session.rollback()
        print("Commit failed:", e)

    admin01  = datastore.find_user(email="admin@gmail.com")
    doctor01 = datastore.find_user(email="doctor@gmail.com")
    patient01= datastore.find_user(email="patient@gmail.com")

    # reuse the role objects created earlier (they are in admin_role/doctor_role/patient_role)
    datastore.add_role_to_user(admin01,  admin_role)
    datastore.add_role_to_user(doctor01, doctor_role)
    datastore.add_role_to_user(patient01,patient_role)
    
    try:
        db.session.commit()
        print("✅ Added roles")
    except Exception as e:
        db.session.rollback()
        print("Failed adding roles:", e)
