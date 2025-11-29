import uuid  # <--- IMPORT THIS
from flask import Blueprint, request, jsonify, current_app
from flask_security.utils import verify_password, hash_password
from models import User, db,Patient

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not verify_password(password, user.password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.active:
        return jsonify({"error": "Account is not active. Please contact admin."}), 403

    try:
        user.fs_uniquifier = str(uuid.uuid4())
        db.session.commit()
        
  
        token = user.get_auth_token()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error generating token", "error": str(e)}), 500

    roles = [role.name for role in user.roles]

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id, 
            "name": user.name,
            "email": user.email,
            "roles": roles,
            "token": token,
            "address": user.address,
            "pincode": user.pincode
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    pincode = data.get('pincode')

    if not name or not email or not password:
        return jsonify({"message": "Name, email, and password are required"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    datastore = current_app.datastore

    try:
   
        user = datastore.create_user(
            name=name, 
            email=email, 
            password=hash_password(password),
            address=address, 
            pincode=pincode, 
            active=True 
        )
        
    
        db.session.flush() 
        print(f"Created User with ID: {user.id}") 
       
        patient_role = datastore.find_role('patient')
        datastore.add_role_to_user(user, patient_role)
        
      
        new_patient_profile = Patient(user_id=user.id, contact_info="N/A")
        db.session.add(new_patient_profile)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "details": str(e)}), 500

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": "patient"
        }
    }), 201