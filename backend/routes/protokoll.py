from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select
from datetime import datetime

protokoll_bp = Blueprint('protokoll', __name__, url_prefix='/api/protokoll')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @protokoll_bp.route('', methods=['GET'])
    def get_protocols():
        """Get all protocols with resolved appointment data"""
        try:
            with db.session as session:
                protocols = session.execute(select(tables.Protokoll)).scalars().all()
                result = []
                for protocol in protocols:
                    # Resolve Termine foreign key
                    termin = session.execute(
                        select(tables.Termine).where(tables.Termine.id == protocol.Termin)
                    ).scalar_one_or_none()
                    
                    protocol_data = {
                        "id": protocol.id,
                        "datum": protocol.Datum.isoformat() if protocol.Datum else None,
                        "text": protocol.Text,
                        "dauer": protocol.Dauer,
                        "tldr": protocol.TLDR,
                        "termin_id": protocol.Termin
                    }
                    
                    if termin:
                        # Also resolve Terminart for the termin
                        art = session.execute(
                            select(tables.Terminart).where(tables.Terminart.id == termin.Art)
                        ).scalar_one_or_none()
                        
                        protocol_data["termin"] = {
                            "id": termin.id,
                            "title": termin.Titel,
                            "ort": termin.Ort,
                            "art_id": termin.Art,
                            "start": termin.Start.isoformat() if termin.Start else None,
                            "ende": termin.Ende.isoformat() if termin.Ende else None,
                            "uid": termin.Uid
                        }
                        
                        if art:
                            protocol_data["termin"]["art"] = {
                                "id": art.id,
                                "name": art.Name
                            }
                    
                    result.append(protocol_data)
                return jsonify({"protocols": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @protokoll_bp.route('/<int:protocol_id>', methods=['GET'])
    def get_protocol(protocol_id):
        """Get a single protocol by ID with resolved appointment data"""
        try:
            with db.session as session:
                protocol = session.execute(
                    select(tables.Protokoll).where(tables.Protokoll.id == protocol_id)
                ).scalar_one_or_none()
                
                if protocol:
                    # Resolve Termine foreign key
                    termin = session.execute(
                        select(tables.Termine).where(tables.Termine.id == protocol.Termin)
                    ).scalar_one_or_none()
                    
                    protocol_data = {
                        "id": protocol.id,
                        "datum": protocol.Datum.isoformat() if protocol.Datum else None,
                        "text": protocol.Text,
                        "dauer": protocol.Dauer,
                        "tldr": protocol.TLDR,
                        "termin_id": protocol.Termin
                    }
                    
                    if termin:
                        # Also resolve Terminart for the termin
                        art = session.execute(
                            select(tables.Terminart).where(tables.Terminart.id == termin.Art)
                        ).scalar_one_or_none()
                        
                        protocol_data["termin"] = {
                            "id": termin.id,
                            "title": termin.Titel,
                            "ort": termin.Ort,
                            "art_id": termin.Art,
                            "start": termin.Start.isoformat() if termin.Start else None,
                            "ende": termin.Ende.isoformat() if termin.Ende else None,
                            "uid": termin.Uid
                        }
                        
                        if art:
                            protocol_data["termin"]["art"] = {
                                "id": art.id,
                                "name": art.Name
                            }
                    
                    return jsonify(protocol_data), 200
                else:
                    return jsonify({"error": "Protocol not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @protokoll_bp.route('', methods=['POST'])
    def create_protocol():
        """Create a new protocol"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['datum', 'text', 'dauer', 'tldr', 'termin_id']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                # Parse datetime
                datum = datetime.fromisoformat(data['datum'])
                
                new_protocol = tables.Protokoll(
                    Datum=datum,
                    Text=data['text'],
                    Dauer=data['dauer'],
                    TLDR=data['tldr'],
                    Termin=data['termin_id']
                )
                session.add(new_protocol)
                session.commit()
                session.refresh(new_protocol)
                
                return jsonify({
                    "id": new_protocol.id,
                    "datum": new_protocol.Datum.isoformat(),
                    "text": new_protocol.Text,
                    "dauer": new_protocol.Dauer,
                    "tldr": new_protocol.TLDR,
                    "termin_id": new_protocol.Termin
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @protokoll_bp.route('/<int:protocol_id>', methods=['PUT'])
    def update_protocol(protocol_id):
        """Update an existing protocol"""
        try:
            data = request.get_json()
            
            with db.session as session:
                protocol = session.execute(
                    select(tables.Protokoll).where(tables.Protokoll.id == protocol_id)
                ).scalar_one_or_none()
                
                if not protocol:
                    return jsonify({"error": "Protocol not found"}), 404
                
                # Update fields if provided
                if 'datum' in data:
                    protocol.Datum = datetime.fromisoformat(data['datum'])
                if 'text' in data:
                    protocol.Text = data['text']
                if 'dauer' in data:
                    protocol.Dauer = data['dauer']
                if 'tldr' in data:
                    protocol.TLDR = data['tldr']
                if 'termin_id' in data:
                    protocol.Termin = data['termin_id']
                
                session.commit()
                session.refresh(protocol)
                
                return jsonify({
                    "id": protocol.id,
                    "datum": protocol.Datum.isoformat(),
                    "text": protocol.Text,
                    "dauer": protocol.Dauer,
                    "tldr": protocol.TLDR,
                    "termin_id": protocol.Termin
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @protokoll_bp.route('/<int:protocol_id>', methods=['DELETE'])
    def delete_protocol(protocol_id):
        """Delete a protocol"""
        try:
            with db.session as session:
                protocol = session.execute(
                    select(tables.Protokoll).where(tables.Protokoll.id == protocol_id)
                ).scalar_one_or_none()
                
                if not protocol:
                    return jsonify({"error": "Protocol not found"}), 404
                
                session.delete(protocol)
                session.commit()
                
                return jsonify({"message": "Protocol deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return protokoll_bp
