from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

teilnehmer_bp = Blueprint('teilnehmer', __name__, url_prefix='/api/teilnehmer')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @teilnehmer_bp.route('', methods=['GET'])
    def get_participants():
        """Get all participants"""
        try:
            with db.session as session:
                participants = session.execute(select(tables.Teilnehmer)).scalars().all()
                result = []
                for participant in participants:
                    result.append({
                        "id": participant.id,
                        "kontakt_id": participant.Kontakt,
                        "termin_id": participant.Termin
                    })
                return jsonify({"participants": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @teilnehmer_bp.route('/<int:participant_id>', methods=['GET'])
    def get_participant(participant_id):
        """Get a single participant by ID"""
        try:
            with db.session as session:
                participant = session.execute(
                    select(tables.Teilnehmer).where(tables.Teilnehmer.id == participant_id)
                ).scalar_one_or_none()
                
                if participant:
                    return jsonify({
                        "id": participant.id,
                        "kontakt_id": participant.Kontakt,
                        "termin_id": participant.Termin
                    }), 200
                else:
                    return jsonify({"error": "Participant not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @teilnehmer_bp.route('', methods=['POST'])
    def create_participant():
        """Create a new participant"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['kontakt_id', 'termin_id']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_participant = tables.Teilnehmer(
                    Kontakt=data['kontakt_id'],
                    Termin=data['termin_id']
                )
                session.add(new_participant)
                session.commit()
                session.refresh(new_participant)
                
                return jsonify({
                    "id": new_participant.id,
                    "kontakt_id": new_participant.Kontakt,
                    "termin_id": new_participant.Termin
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @teilnehmer_bp.route('/<int:participant_id>', methods=['PUT'])
    def update_participant(participant_id):
        """Update an existing participant"""
        try:
            data = request.get_json()
            
            with db.session as session:
                participant = session.execute(
                    select(tables.Teilnehmer).where(tables.Teilnehmer.id == participant_id)
                ).scalar_one_or_none()
                
                if not participant:
                    return jsonify({"error": "Participant not found"}), 404
                
                # Update fields if provided
                if 'kontakt_id' in data:
                    participant.Kontakt = data['kontakt_id']
                if 'termin_id' in data:
                    participant.Termin = data['termin_id']
                
                session.commit()
                session.refresh(participant)
                
                return jsonify({
                    "id": participant.id,
                    "kontakt_id": participant.Kontakt,
                    "termin_id": participant.Termin
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @teilnehmer_bp.route('/<int:participant_id>', methods=['DELETE'])
    def delete_participant(participant_id):
        """Delete a participant"""
        try:
            with db.session as session:
                participant = session.execute(
                    select(tables.Teilnehmer).where(tables.Teilnehmer.id == participant_id)
                ).scalar_one_or_none()
                
                if not participant:
                    return jsonify({"error": "Participant not found"}), 404
                
                session.delete(participant)
                session.commit()
                
                return jsonify({"message": "Participant deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return teilnehmer_bp
