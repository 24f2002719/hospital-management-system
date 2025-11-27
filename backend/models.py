from database import db
from datetime import datetime, timezone, timedelta
from sqlalchemy import Enum
from sqlalchemy.schema import UniqueConstraint
import enum
from flask_security import UserMixin, RoleMixin
# import jwt  <-- REMOVED: Not needed, Flask-Security handles this
from flask import current_app

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc))
    
class Specialization(BaseModel):
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

class User(BaseModel, UserMixin): # UserMixin provides the correct get_auth_token
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    
    # Flask-Security fields
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True) 
    roles = db.relationship('Role', backref='bearers', secondary='user_roles')
    
    # Profiles
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)

    address = db.Column(db.String(250), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)

    # REMOVED: def get_auth_token(self)... 
    # We let Flask-Security's UserMixin handle this method now.

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
    available_slots = db.Column(db.String(255)) 
    
    __table_args__ = (UniqueConstraint('doctor_id', 'available_date', name='_doctor_date_uc'),)