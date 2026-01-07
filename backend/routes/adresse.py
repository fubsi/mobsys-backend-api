from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

adresse_bp = Blueprint('adresse', __name__, url_prefix='/api/adresse')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @adresse_bp.route('', methods=['GET'])
    def get_addresses():
        """Get all addresses"""
        try:
            with db.session as session:
                addresses = session.execute(select(tables.Adresse)).scalars().all()
                result = []
                for address in addresses:
                    result.append({
                        "id": address.id,
                        "plz": address.Plz,
                        "ortsname": address.ortsname,
                        "strasse": address.Strasse,
                        "hausnr": address.Hausnr
                    })
                return jsonify({"addresses": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @adresse_bp.route('/<int:address_id>', methods=['GET'])
    def get_address(address_id):
        """Get a single address by ID"""
        try:
            with db.session as session:
                address = session.execute(
                    select(tables.Adresse).where(tables.Adresse.id == address_id)
                ).scalar_one_or_none()
                
                if address:
                    return jsonify({
                        "id": address.id,
                        "plz": address.Plz,
                        "ortsname": address.ortsname,
                        "strasse": address.Strasse,
                        "hausnr": address.Hausnr
                    }), 200
                else:
                    return jsonify({"error": "Address not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @adresse_bp.route('', methods=['POST'])
    def create_address():
        """Create a new address"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['plz', 'ortsname', 'strasse', 'hausnr']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_address = tables.Adresse(
                    Plz=data['plz'],
                    ortsname=data['ortsname'],
                    Strasse=data['strasse'],
                    Hausnr=data['hausnr']
                )
                session.add(new_address)
                session.commit()
                session.refresh(new_address)
                
                return jsonify({
                    "id": new_address.id,
                    "plz": new_address.Plz,
                    "ortsname": new_address.ortsname,
                    "strasse": new_address.Strasse,
                    "hausnr": new_address.Hausnr
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @adresse_bp.route('/<int:address_id>', methods=['PUT'])
    def update_address(address_id):
        """Update an existing address"""
        try:
            data = request.get_json()
            
            with db.session as session:
                address = session.execute(
                    select(tables.Adresse).where(tables.Adresse.id == address_id)
                ).scalar_one_or_none()
                
                if not address:
                    return jsonify({"error": "Address not found"}), 404
                
                # Update fields if provided
                if 'plz' in data:
                    address.Plz = data['plz']
                if 'ortsname' in data:
                    address.ortsname = data['ortsname']
                if 'strasse' in data:
                    address.Strasse = data['strasse']
                if 'hausnr' in data:
                    address.Hausnr = data['hausnr']
                
                session.commit()
                session.refresh(address)
                
                return jsonify({
                    "id": address.id,
                    "plz": address.Plz,
                    "ortsname": address.ortsname,
                    "strasse": address.Strasse,
                    "hausnr": address.Hausnr
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @adresse_bp.route('/<int:address_id>', methods=['DELETE'])
    def delete_address(address_id):
        """Delete an address"""
        try:
            with db.session as session:
                address = session.execute(
                    select(tables.Adresse).where(tables.Adresse.id == address_id)
                ).scalar_one_or_none()
                
                if not address:
                    return jsonify({"error": "Address not found"}), 404
                
                session.delete(address)
                session.commit()
                
                return jsonify({"message": "Address deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return adresse_bp
