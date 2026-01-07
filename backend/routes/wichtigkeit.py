from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

wichtigkeit_bp = Blueprint('wichtigkeit', __name__, url_prefix='/api/wichtigkeit')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @wichtigkeit_bp.route('', methods=['GET'])
    def get_importances():
        """Get all importance levels"""
        try:
            with db.session as session:
                importances = session.execute(select(tables.Wichtigkeit)).scalars().all()
                result = []
                for importance in importances:
                    result.append({
                        "id": importance.id,
                        "level": importance.level
                    })
                return jsonify({"importance_levels": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @wichtigkeit_bp.route('/<int:importance_id>', methods=['GET'])
    def get_importance(importance_id):
        """Get a single importance level by ID"""
        try:
            with db.session as session:
                importance = session.execute(
                    select(tables.Wichtigkeit).where(tables.Wichtigkeit.id == importance_id)
                ).scalar_one_or_none()
                
                if importance:
                    return jsonify({
                        "id": importance.id,
                        "level": importance.level
                    }), 200
                else:
                    return jsonify({"error": "Importance level not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @wichtigkeit_bp.route('', methods=['POST'])
    def create_importance():
        """Create a new importance level"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'level' not in data:
                return jsonify({"error": "Missing required field: level"}), 400
            
            with db.session as session:
                new_importance = tables.Wichtigkeit(
                    level=data['level']
                )
                session.add(new_importance)
                session.commit()
                session.refresh(new_importance)
                
                return jsonify({
                    "id": new_importance.id,
                    "level": new_importance.level
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @wichtigkeit_bp.route('/<int:importance_id>', methods=['PUT'])
    def update_importance(importance_id):
        """Update an existing importance level"""
        try:
            data = request.get_json()
            
            with db.session as session:
                importance = session.execute(
                    select(tables.Wichtigkeit).where(tables.Wichtigkeit.id == importance_id)
                ).scalar_one_or_none()
                
                if not importance:
                    return jsonify({"error": "Importance level not found"}), 404
                
                # Update fields if provided
                if 'level' in data:
                    importance.level = data['level']
                
                session.commit()
                session.refresh(importance)
                
                return jsonify({
                    "id": importance.id,
                    "level": importance.level
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @wichtigkeit_bp.route('/<int:importance_id>', methods=['DELETE'])
    def delete_importance(importance_id):
        """Delete an importance level"""
        try:
            with db.session as session:
                importance = session.execute(
                    select(tables.Wichtigkeit).where(tables.Wichtigkeit.id == importance_id)
                ).scalar_one_or_none()
                
                if not importance:
                    return jsonify({"error": "Importance level not found"}), 404
                
                session.delete(importance)
                session.commit()
                
                return jsonify({"message": "Importance level deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return wichtigkeit_bp
