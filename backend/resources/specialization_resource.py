from flask import request
from flask_restful import Resource
from services.specialization_service import SpecializationService


def spec_to_dict(spec):
    return {
        "id": spec.id,
        "name": spec.name,
        "description": spec.description,
        "created_at": str(spec.created_at)
    }

class SpecializationListResource(Resource):
    
    def get(self):
        """ GET /api/specializations """
        specs = SpecializationService.get_all_specializations()
        return [spec_to_dict(s) for s in specs], 200

    def post(self):
        """ POST /api/specializations """
        data = request.get_json()
        
        if not data.get('name'):
            return {"message": "Name is required"}, 400

        spec, message = SpecializationService.create_specialization(
            name=data.get('name'),
            description=data.get('description', '')
        )

        if not spec:
            return {"message": message}, 400

        return spec_to_dict(spec), 201


class SpecializationResource(Resource):
    
    def get(self, spec_id):
        """ GET /api/specializations/<id> """
        spec = SpecializationService.get_specialization_by_id(spec_id)
        if not spec:
            return {"message": "Not Found"}, 404
        return spec_to_dict(spec), 200

    def put(self, spec_id):
        """ PUT /api/specializations/<id> """
        data = request.get_json()
        spec, message = SpecializationService.update_specialization(spec_id, data)
        
        if not spec:
            return {"message": message}, 400
        return spec_to_dict(spec), 200

    def delete(self, spec_id):
        """ DELETE /api/specializations/<id> """
        success, message = SpecializationService.delete_specialization(spec_id)
        
        if success:
            return {"message": message}, 200
        return {"message": message}, 400