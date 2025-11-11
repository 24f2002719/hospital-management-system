from database import db
from datetime import datetime, timezone
from sqlalchemy import Enum
from sqlalchemy.schema import UniqueConstraint
import enum
from flask_security import UserMixin, RoleMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc))
    
class Specialization(BaseModel):
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

# class Role(enum.Enum):
#     ADMIN = 'admin'
#     DOCTOR = 'doctor'
#     PATIENT = 'patient'
    
class User(BaseModel):
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    # for flask-security-too
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True) 
    # if Active = False, then the user will not be able to login
    roles = db.relationship('Role', backref='bearers', secondary='user_roles')
    is_active = db.Column(db.Boolean, default=True) # Blacklist feature


    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)

    address = db.Column(db.String(250), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)

class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class AppointmentStatus(enum.Enum):
    BOOKED = 'Booked'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'



class Doctor(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    
    specialization = db.relationship('Specialization', backref='doctors')
    availabilities = db.relationship('DoctorAvailability', backref='doctor', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')

class Patient(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    contact_info = db.Column(db.String(15))
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')

class Appointment(BaseModel):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(5), nullable=False) # HH:MM format
    status = db.Column(Enum(AppointmentStatus), default=AppointmentStatus.BOOKED)

    treatment = db.relationship('Treatment', backref='appointment', uselist=False)
    
    # Milestone 7 requirement: Prevent double booking
    __table_args__ = (UniqueConstraint('doctor_id', 'appointment_date', 'appointment_time', name='_doctor_time_uc'),)

class Treatment(BaseModel):
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), unique=True, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    next_visit_suggested = db.Column(db.Date)

class DoctorAvailability(BaseModel):
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    available_slots = db.Column(db.String(255)) # e.g., "09:00,10:00,11:00"
    
    __table_args__ = (UniqueConstraint('doctor_id', 'available_date', name='_doctor_date_uc'),)



