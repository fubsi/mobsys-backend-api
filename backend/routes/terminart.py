from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

terminart_bp = Blueprint('terminart', __name__, url_prefix='/api/terminart')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @terminart_bp.route('', methods=['GET'])
    def get_appointment_types():
        """Get all appointment types"""
        try:
            with db.session as session:
                types = session.execute(select(tables.Terminart)).scalars().all()
                result = []
                for type_obj in types:
                    result.append({
                        "id": type_obj.id,
                        "name": type_obj.Name
                    })
                return jsonify({"appointment_types": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @terminart_bp.route('/<int:type_id>', methods=['GET'])
    def get_appointment_type(type_id):
        """Get a single appointment type by ID"""
        try:
            with db.session as session:
                type_obj = session.execute(
                    select(tables.Terminart).where(tables.Terminart.id == type_id)
                ).scalar_one_or_none()
                
                if type_obj:
                    return jsonify({
                        "id": type_obj.id,
                        "name": type_obj.Name
                    }), 200
                else:
                    return jsonify({"error": "Appointment type not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @terminart_bp.route('', methods=['POST'])
    def create_appointment_type():
        """Create a new appointment type"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'name' not in data:
                return jsonify({"error": "Missing required field: name"}), 400
            
            with db.session as session:
                new_type = tables.Terminart(
                    Name=data['name']
                )
                session.add(new_type)
                session.commit()
                session.refresh(new_type)
                
                return jsonify({
                    "id": new_type.id,
                    "name": new_type.Name
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @terminart_bp.route('/<int:type_id>', methods=['PUT'])
    def update_appointment_type(type_id):
        """Update an existing appointment type"""
        try:
            data = request.get_json()
            
            with db.session as session:
                type_obj = session.execute(
                    select(tables.Terminart).where(tables.Terminart.id == type_id)
                ).scalar_one_or_none()
                
                if not type_obj:
                    return jsonify({"error": "Appointment type not found"}), 404
                
                # Update fields if provided
                if 'name' in data:
                    type_obj.Name = data['name']
                
                session.commit()
                session.refresh(type_obj)
                
                return jsonify({
                    "id": type_obj.id,
                    "name": type_obj.Name
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @terminart_bp.route('/<int:type_id>', methods=['DELETE'])
    def delete_appointment_type(type_id):
        """Delete an appointment type"""
        try:
            with db.session as session:
                type_obj = session.execute(
                    select(tables.Terminart).where(tables.Terminart.id == type_id)
                ).scalar_one_or_none()
                
                if not type_obj:
                    return jsonify({"error": "Appointment type not found"}), 404
                
                session.delete(type_obj)
                session.commit()
                
                return jsonify({"message": "Appointment type deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return terminart_bp
