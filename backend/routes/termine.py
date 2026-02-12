from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select
from datetime import datetime

termine_bp = Blueprint('termine', __name__, url_prefix='/api/termine')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @termine_bp.route('', methods=['GET'])
    def get_appointments():
        """Get all appointments with resolved appointment type data"""
        try:
            with db.session as session:
                appointments = session.execute(select(tables.Termine)).scalars().all()
                result = []
                for appointment in appointments:
                    # Resolve Terminart foreign key
                    art = session.execute(
                        select(tables.Terminart).where(tables.Terminart.id == appointment.Art)
                    ).scalar_one_or_none()
                    
                    appointment_data = {
                        "id": appointment.id,
                        "title": appointment.Titel,
                        "ort": appointment.Ort,
                        "art_id": appointment.Art,
                        "start": appointment.Start.isoformat() if appointment.Start else None,
                        "ende": appointment.Ende.isoformat() if appointment.Ende else None,
                        "uid": appointment.Uid
                    }
                    
                    if art:
                        appointment_data["art"] = {
                            "id": art.id,
                            "name": art.Name
                        }
                    
                    result.append(appointment_data)
                return jsonify({"appointments": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @termine_bp.route('/<int:appointment_id>', methods=['GET'])
    def get_appointment(appointment_id):
        """Get a single appointment by ID with resolved appointment type data"""
        try:
            with db.session as session:
                appointment = session.execute(
                    select(tables.Termine).where(tables.Termine.id == appointment_id)
                ).scalar_one_or_none()
                
                if appointment:
                    # Resolve Terminart foreign key
                    art = session.execute(
                        select(tables.Terminart).where(tables.Terminart.id == appointment.Art)
                    ).scalar_one_or_none()
                    
                    appointment_data = {
                        "id": appointment.id,
                        "title": appointment.Titel,
                        "ort": appointment.Ort,
                        "art_id": appointment.Art,
                        "start": appointment.Start.isoformat() if appointment.Start else None,
                        "ende": appointment.Ende.isoformat() if appointment.Ende else None,
                        "uid": appointment.Uid
                    }
                    
                    if art:
                        appointment_data["art"] = {
                            "id": art.id,
                            "name": art.Name
                        }
                    
                    return jsonify(appointment_data), 200
                else:
                    return jsonify({"error": "Appointment not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @termine_bp.route('', methods=['POST'])
    def create_appointment():
        """Create a new appointment"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['title', 'ort', 'art_id', 'start', 'ende', 'uid']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                # Parse datetime
                start = datetime.fromisoformat(data['start'])
                ende = datetime.fromisoformat(data['ende'])
                
                new_appointment = tables.Termine(
                    Titel=data['title'],
                    Ort=data['ort'],
                    Art=data['art_id'],
                    Start=start,
                    Ende=ende,
                    Uid=data['uid']
                )
                session.add(new_appointment)
                session.commit()
                session.refresh(new_appointment)
                
                return jsonify({
                    "id": new_appointment.id,
                    "title": new_appointment.Titel,
                    "ort": new_appointment.Ort,
                    "art_id": new_appointment.Art,
                    "start": new_appointment.Start.isoformat(),
                    "ende": new_appointment.Ende.isoformat(),
                    "uid": new_appointment.Uid
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @termine_bp.route('/<int:appointment_id>', methods=['PUT'])
    def update_appointment(appointment_id):
        """Update an existing appointment"""
        try:
            data = request.get_json()
            
            with db.session as session:
                appointment = session.execute(
                    select(tables.Termine).where(tables.Termine.id == appointment_id)
                ).scalar_one_or_none()
                
                if not appointment:
                    return jsonify({"error": "Appointment not found"}), 404
                
                # Update fields if provided
                if 'title' in data:
                    appointment.Titel = data['title']
                if 'ort' in data:
                    appointment.Ort = data['ort']
                if 'art_id' in data:
                    appointment.Art = data['art_id']
                if 'start' in data:
                    appointment.Start = datetime.fromisoformat(data['start'])
                if 'ende' in data:
                    appointment.Ende = datetime.fromisoformat(data['ende'])
                if 'uid' in data:
                    appointment.Uid = data['uid']
                
                session.commit()
                session.refresh(appointment)
                
                return jsonify({
                    "id": appointment.id,
                    "title": appointment.Titel,
                    "ort": appointment.Ort,
                    "art_id": appointment.Art,
                    "start": appointment.Start.isoformat(),
                    "ende": appointment.Ende.isoformat(),
                    "uid": appointment.Uid
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @termine_bp.route('/<int:appointment_id>', methods=['DELETE'])
    def delete_appointment(appointment_id):
        """Delete an appointment"""
        try:
            with db.session as session:
                appointment = session.execute(
                    select(tables.Termine).where(tables.Termine.id == appointment_id)
                ).scalar_one_or_none()
                
                if not appointment:
                    return jsonify({"error": "Appointment not found"}), 404
                
                session.delete(appointment)
                session.commit()
                
                return jsonify({"message": "Appointment deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return termine_bp
