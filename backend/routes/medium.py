from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

medium_bp = Blueprint('medium', __name__, url_prefix='/api/medium')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @medium_bp.route('', methods=['GET'])
    def get_media():
        """Get all media"""
        try:
            with db.session as session:
                media = session.execute(select(tables.Medium)).scalars().all()
                result = []
                for medium in media:
                    result.append({
                        "id": medium.id,
                        "dateityp": medium.Dateityp,
                        "dateiname": medium.Dateiname
                    })
                return jsonify({"media": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @medium_bp.route('/<int:medium_id>', methods=['GET'])
    def get_medium(medium_id):
        """Get a single medium by ID"""
        try:
            with db.session as session:
                medium = session.execute(
                    select(tables.Medium).where(tables.Medium.id == medium_id)
                ).scalar_one_or_none()
                
                if medium:
                    return jsonify({
                        "id": medium.id,
                        "dateityp": medium.Dateityp,
                        "dateiname": medium.Dateiname
                    }), 200
                else:
                    return jsonify({"error": "Medium not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @medium_bp.route('', methods=['POST'])
    def create_medium():
        """Create a new medium"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['dateityp', 'dateiname']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_medium = tables.Medium(
                    Dateityp=data['dateityp'],
                    Dateiname=data['dateiname']
                )
                session.add(new_medium)
                session.commit()
                session.refresh(new_medium)
                
                return jsonify({
                    "id": new_medium.id,
                    "dateityp": new_medium.Dateityp,
                    "dateiname": new_medium.Dateiname
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @medium_bp.route('/<int:medium_id>', methods=['PUT'])
    def update_medium(medium_id):
        """Update an existing medium"""
        try:
            data = request.get_json()
            
            with db.session as session:
                medium = session.execute(
                    select(tables.Medium).where(tables.Medium.id == medium_id)
                ).scalar_one_or_none()
                
                if not medium:
                    return jsonify({"error": "Medium not found"}), 404
                
                # Update fields if provided
                if 'dateityp' in data:
                    medium.Dateityp = data['dateityp']
                if 'dateiname' in data:
                    medium.Dateiname = data['dateiname']
                
                session.commit()
                session.refresh(medium)
                
                return jsonify({
                    "id": medium.id,
                    "dateityp": medium.Dateityp,
                    "dateiname": medium.Dateiname
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @medium_bp.route('/<int:medium_id>', methods=['DELETE'])
    def delete_medium(medium_id):
        """Delete a medium"""
        try:
            with db.session as session:
                medium = session.execute(
                    select(tables.Medium).where(tables.Medium.id == medium_id)
                ).scalar_one_or_none()
                
                if not medium:
                    return jsonify({"error": "Medium not found"}), 404
                
                session.delete(medium)
                session.commit()
                
                return jsonify({"message": "Medium deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return medium_bp
