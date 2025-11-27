from models import User, Doctor, Specialization, Role, db
from flask_security import current_user
from flask_security.utils import hash_password
from flask import current_app

class UserService:
    
    @staticmethod
    def get_all_users():
        """Admin Only: Get all users"""
        if not current_user.has_role('admin'):
            return {"error": "Unauthorized"}, 403

        users = User.query.all()
        result = []
        for user in users:
            roles = [r.name for r in user.roles]
            
            # Identify user type
            user_type = "Admin"
            spec = None
            if user.doctor_profile:
                user_type = "Doctor"
                spec = user.doctor_profile.specialization.name
            elif user.patient_profile:
                user_type = "Patient"

            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "roles": roles,
                "type": user_type,
                "specialization": spec,
                "active": user.active
            })
        return result, 200

    @staticmethod
    def create_doctor(data):
        """Admin Only: Create a new Doctor"""
        if not current_user.has_role('admin'):
            return {"error": "Unauthorized"}, 403

        email = data.get('email')
        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400

        # Validate Specialization
        spec_name = data.get('specialization')
        specialization = Specialization.query.filter_by(name=spec_name).first()
        if not specialization:
            return {"error": f"Specialization '{spec_name}' not found"}, 404

        datastore = current_app.datastore
        try:
            # 1. Create User
            user = datastore.create_user(
                name=data.get('name'),
                email=email,
                password=hash_password(data.get('password')),
                address=data.get('address'),
                pincode=data.get('pincode'),
                active=True
            )
            
            # 2. Add Role
            doctor_role = datastore.find_role('doctor')
            datastore.add_role_to_user(user, doctor_role)
            
            # 3. Create Doctor Profile
            new_doc = Doctor(user_id=user.id, specialization_id=specialization.id)
            db.session.add(new_doc)
            db.session.commit()
            
            return {"message": "Doctor created successfully", "id": user.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_user(user_id):
        """Admin or Owner can view profile"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        if not (current_user.has_role('admin') or current_user.id == user.id):
            return {"error": "Unauthorized"}, 403

        roles = [r.name for r in user.roles]
        resp = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode,
            "roles": roles,
            "active": user.active
        }

        if user.doctor_profile:
            resp['specialization'] = user.doctor_profile.specialization.name
        
        if user.patient_profile:
            resp['contact_info'] = user.patient_profile.contact_info

        return resp, 200

    @staticmethod
    def update_user(user_id, data):
        """Admin (all fields) or Owner (limited fields) can update"""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        is_admin = current_user.has_role('admin')
        is_owner = current_user.id == user.id

        if not (is_admin or is_owner):
            return {"error": "Unauthorized"}, 403

        try:
            # Common updates
            if 'name' in data: user.name = data['name']
            if 'address' in data: user.address = data['address']
            if 'pincode' in data: user.pincode = data['pincode']

            # Admin only updates
            if is_admin:
                if 'active' in data: user.active = data['active']
                
                # Update Specialization if user is a doctor
                if 'specialization' in data and user.doctor_profile:
                    spec = Specialization.query.filter_by(name=data['specialization']).first()
                    if spec:
                        user.doctor_profile.specialization = spec
                    else:
                        return {"error": "Specialization not found"}, 404

            db.session.commit()
            return {"message": "User updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete_user(user_id):
        """Admin only delete with Cascade Cleanup"""
        if not current_user.has_role('admin'):
            return {"error": "Unauthorized"}, 403

        if user_id == current_user.id:
            return {"error": "Operation denied. You cannot delete your own account."}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            # 1. CLEANUP DOCTOR DATA
            if user.doctor_profile:
                doctor = user.doctor_profile
                
                # A. Delete Appointments linked to this Doctor
                # (We iterate to ensure Treatments are deleted too)
                for appointment in doctor.appointments:
                    if appointment.treatment:
                        db.session.delete(appointment.treatment) # Delete Treatment first
                    db.session.delete(appointment) # Then delete Appointment
                
                # B. Delete Availabilities
                for availability in doctor.availabilities:
                    db.session.delete(availability)
                
                # C. Delete the Doctor Profile
                db.session.delete(doctor)

            # 2. CLEANUP PATIENT DATA
            if user.patient_profile:
                patient = user.patient_profile
                
                # A. Delete Appointments linked to this Patient
                for appointment in patient.appointments:
                    if appointment.treatment:
                        db.session.delete(appointment.treatment)
                    db.session.delete(appointment)
                
                # B. Delete Patient Profile
                db.session.delete(patient)

            # 3. DELETE USER ROLES (Clean up association table)
            user.roles = [] 

            # 4. FINALLY DELETE THE USER
            db.session.delete(user)
            db.session.commit()
            
            return {"message": "User and all associated data deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            # Log the actual error for debugging
            print(f"Delete Error: {str(e)}")
            return {"error": "Cannot delete user. Database constraint violation.", "details": str(e)}, 400