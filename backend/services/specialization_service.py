from models import db, Specialization
from sqlalchemy.exc import IntegrityError

class SpecializationService:

    @staticmethod
    def create_specialization(name, description):
        # 1. Check if it already exists (Optional optimization, but DB will catch it too)
        existing = Specialization.query.filter_by(name=name).first()
        if existing:
            return None, f"Specialization '{name}' already exists."

        # 2. Create Object
        new_spec = Specialization(
            name=name,
            description=description
        )

        try:
            db.session.add(new_spec)
            db.session.commit()
            
            # 🔥 Refresh to get the generated ID
            db.session.refresh(new_spec)
            return new_spec, "Specialization created successfully."
            
        except IntegrityError:
            db.session.rollback()
            return None, "Specialization with this name already exists."
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_all_specializations():
        return Specialization.query.all()

    @staticmethod
    def get_specialization_by_id(spec_id):
        return Specialization.query.get(spec_id)

    @staticmethod
    def update_specialization(spec_id, data):
        spec = Specialization.query.get(spec_id)
        if not spec:
            return None, "Specialization not found"

        if 'name' in data:
            spec.name = data['name']
        if 'description' in data:
            spec.description = data['description']

        try:
            db.session.commit()
            db.session.refresh(spec)
            return spec, "Updated successfully."
        except IntegrityError:
            db.session.rollback()
            return None, "Name already taken by another specialization."
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_specialization(spec_id):
        spec = Specialization.query.get(spec_id)
        if not spec:
            return False, "Specialization not found"
        
        # Check if any doctors are using this specialization before deleting?
        # For now, we will let SQL handle foreign key errors if they exist.
        try:
            db.session.delete(spec)
            db.session.commit()
            return True, "Deleted successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Cannot delete: {str(e)} (Likely used by a Doctor)"