from app import app
from models import db, User, Patient

with app.app_context():
    print("\n" + "="*40)
    print("   VALID IDS FOR POSTMAN")
    print("="*40)
    
    # 1. Find all Patients
    patients = Patient.query.all()
    
    if not patients:
        print("❌ No patients found! Run 'python seed.py' first.")
    else:
        print(f"Found {len(patients)} patients.\n")
        print(f"{'USER ID':<10} | {'NAME':<20} | {'EMAIL'}")
        print("-" * 50)
        
        for p in patients:
            # We need p.user_id, NOT p.id
            print(f"{p.user_id:<10} | {p.user.name:<20} | {p.user.email}")
            
    print("\n👉 USE THE 'USER ID' COLUMN IN POSTMAN")
    print("="*40 + "\n")