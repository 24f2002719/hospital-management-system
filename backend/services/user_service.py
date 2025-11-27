from models import User, Doctor, Specialization, Role, db
from flask_security import current_user
from flask_security.utils import hash_password
from flask import current_app

class UserService:
    
    @staticmethod
    def get_public_doctors():
        doctors = db.session.query(Doctor, User).join(User, Doctor.user_id == User.id).filter(User.active == True).all()
        result = []
        for doc_profile, user_account in doctors:
            result.append({
                "id": doc_profile.id,
                "user_id": user_account.id,
                "name": user_account.name,
                "specialization": doc_profile.specialization.name if doc_profile.specialization else "General",
                "experience": doc_profile.experience_years,
                "bio": doc_profile.bio,
                "available": True 
            })
        return result, 200

    @staticmethod
    def get_all_users():
        """Admin Only: Get all users with FULL details"""
        if not current_user.has_role('admin'):
            return {"error": "Unauthorized"}, 403

        users = User.query.all()
        result = []
        for user in users:
            roles = [r.name for r in user.roles]
            
            user_type = "Admin"
            spec = None
            exp = 0
            bio = ""

            # Check if user is a doctor to get specific fields
            if user.doctor_profile:
                user_type = "Doctor"
                spec = user.doctor_profile.specialization.name
                exp = user.doctor_profile.experience_years
                bio = user.doctor_profile.bio
            elif user.patient_profile:
                user_type = "Patient"

            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,   # <--- ADDED THIS
                "pincode": user.pincode,   # <--- ADDED THIS
                "roles": roles,
                "type": user_type,
                "specialization": spec,
                "experience": exp,         # <--- ADDED THIS
                "bio": bio,                # <--- ADDED THIS
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

        spec_name = data.get('specialization')
        specialization = Specialization.query.filter_by(name=spec_name).first()
        if not specialization:
            return {"error": f"Specialization '{spec_name}' not found"}, 404

        datastore = current_app.datastore
        try:
            user = datastore.create_user(
                name=data.get('name'),
                email=email,
                password=hash_password(data.get('password')),
                address=data.get('address'),
                pincode=data.get('pincode'),
                active=True
            )
            
            doctor_role = datastore.find_role('doctor')
            datastore.add_role_to_user(user, doctor_role)
            
            # --- UPDATED: Save Experience & Bio ---
            new_doc = Doctor(
                user_id=user.id, 
                specialization_id=specialization.id,
                experience_years=data.get('experience', 0),
                bio=data.get('bio', '')
            )
            # --------------------------------------

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
            # --- NEW FIELDS ---
            resp['experience'] = user.doctor_profile.experience_years
            resp['bio'] = user.doctor_profile.bio
            # ------------------
        
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
            if 'name' in data: user.name = data['name']
            if 'address' in data: user.address = data['address']
            if 'pincode' in data: user.pincode = data['pincode']

            if is_admin:
                if 'active' in data: user.active = data['active']
                
            # Handle Doctor Specific Updates (Admin OR the Doctor themselves)
            if user.doctor_profile:
                # Only admin changes specialization
                if is_admin and 'specialization' in data:
                    spec = Specialization.query.filter_by(name=data['specialization']).first()
                    if spec: user.doctor_profile.specialization = spec
                
                # --- NEW: Update Bio & Experience ---
                if 'experience' in data:
                    user.doctor_profile.experience_years = data['experience']
                if 'bio' in data:
                    user.doctor_profile.bio = data['bio']
                # ------------------------------------

            db.session.commit()
            return {"message": "User updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete_user(user_id):
        if not current_user.has_role('admin'):
            return {"error": "Unauthorized"}, 403

        if user_id == current_user.id:
            return {"error": "Operation denied. You cannot delete your own account."}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            if user.doctor_profile:
                doctor = user.doctor_profile
                for appointment in doctor.appointments:
                    if appointment.treatment:
                        db.session.delete(appointment.treatment)
                    db.session.delete(appointment)
                
                for availability in doctor.availabilities:
                    db.session.delete(availability)
                
                db.session.delete(doctor)

            if user.patient_profile:
                patient = user.patient_profile
                for appointment in patient.appointments:
                    if appointment.treatment:
                        db.session.delete(appointment.treatment)
                    db.session.delete(appointment)
                db.session.delete(patient)

            user.roles = [] 
            db.session.delete(user)
            db.session.commit()
            
            return {"message": "User and all associated data deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            print(f"Delete Error: {str(e)}")
            return {"error": "Cannot delete user. Database constraint violation.", "details": str(e)}, 400