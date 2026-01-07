from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select
from datetime import datetime

person_bp = Blueprint('person', __name__, url_prefix='/api/person')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @person_bp.route('', methods=['GET'])
    def get_persons():
        """Get all persons"""
        try:
            with db.session as session:
                persons = session.execute(select(tables.Person)).scalars().all()
                result = []
                for person in persons:
                    result.append({
                        "id": person.id,
                        "name": person.Name,
                        "adresse_id": person.Adresse,
                        "geburtsdatum": person.Geburtsdatum.isoformat() if person.Geburtsdatum else None,
                        "titel": person.Titel
                    })
                return jsonify({"persons": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @person_bp.route('/<int:person_id>', methods=['GET'])
    def get_person(person_id):
        """Get a single person by ID"""
        try:
            with db.session as session:
                person = session.execute(
                    select(tables.Person).where(tables.Person.id == person_id)
                ).scalar_one_or_none()
                
                if person:
                    return jsonify({
                        "id": person.id,
                        "name": person.Name,
                        "adresse_id": person.Adresse,
                        "geburtsdatum": person.Geburtsdatum.isoformat() if person.Geburtsdatum else None,
                        "titel": person.Titel
                    }), 200
                else:
                    return jsonify({"error": "Person not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @person_bp.route('', methods=['POST'])
    def create_person():
        """Create a new person"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['name', 'adresse_id', 'geburtsdatum', 'titel']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                # Parse date
                geburtsdatum = datetime.fromisoformat(data['geburtsdatum']).date()
                
                new_person = tables.Person(
                    Name=data['name'],
                    Adresse=data['adresse_id'],
                    Geburtsdatum=geburtsdatum,
                    Titel=data['titel']
                )
                session.add(new_person)
                session.commit()
                session.refresh(new_person)
                
                return jsonify({
                    "id": new_person.id,
                    "name": new_person.Name,
                    "adresse_id": new_person.Adresse,
                    "geburtsdatum": new_person.Geburtsdatum.isoformat(),
                    "titel": new_person.Titel
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @person_bp.route('/<int:person_id>', methods=['PUT'])
    def update_person(person_id):
        """Update an existing person"""
        try:
            data = request.get_json()
            
            with db.session as session:
                person = session.execute(
                    select(tables.Person).where(tables.Person.id == person_id)
                ).scalar_one_or_none()
                
                if not person:
                    return jsonify({"error": "Person not found"}), 404
                
                # Update fields if provided
                if 'name' in data:
                    person.Name = data['name']
                if 'adresse_id' in data:
                    person.Adresse = data['adresse_id']
                if 'geburtsdatum' in data:
                    person.Geburtsdatum = datetime.fromisoformat(data['geburtsdatum']).date()
                if 'titel' in data:
                    person.Titel = data['titel']
                
                session.commit()
                session.refresh(person)
                
                return jsonify({
                    "id": person.id,
                    "name": person.Name,
                    "adresse_id": person.Adresse,
                    "geburtsdatum": person.Geburtsdatum.isoformat(),
                    "titel": person.Titel
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @person_bp.route('/<int:person_id>', methods=['DELETE'])
    def delete_person(person_id):
        """Delete a person"""
        try:
            with db.session as session:
                person = session.execute(
                    select(tables.Person).where(tables.Person.id == person_id)
                ).scalar_one_or_none()
                
                if not person:
                    return jsonify({"error": "Person not found"}), 404
                
                session.delete(person)
                session.commit()
                
                return jsonify({"message": "Person deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return person_bp
