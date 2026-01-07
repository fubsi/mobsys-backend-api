from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

unternehmen_bp = Blueprint('unternehmen', __name__, url_prefix='/api/unternehmen')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @unternehmen_bp.route('', methods=['GET'])
    def get_companies():
        """Get all companies"""
        try:
            with db.session as session:
                companies = session.execute(select(tables.Unternehmen)).scalars().all()
                result = []
                for company in companies:
                    result.append({
                        "id": company.id,
                        "name": company.Name,
                        "adresse_id": company.Adresse,
                        "umsatz": company.Umsatz
                    })
                return jsonify({"companies": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @unternehmen_bp.route('/<int:company_id>', methods=['GET'])
    def get_company(company_id):
        """Get a single company by ID"""
        try:
            with db.session as session:
                company = session.execute(
                    select(tables.Unternehmen).where(tables.Unternehmen.id == company_id)
                ).scalar_one_or_none()
                
                if company:
                    return jsonify({
                        "id": company.id,
                        "name": company.Name,
                        "adresse_id": company.Adresse,
                        "umsatz": company.Umsatz
                    }), 200
                else:
                    return jsonify({"error": "Company not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @unternehmen_bp.route('', methods=['POST'])
    def create_company():
        """Create a new company"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['name', 'adresse_id', 'umsatz']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_company = tables.Unternehmen(
                    Name=data['name'],
                    Adresse=data['adresse_id'],
                    Umsatz=data['umsatz']
                )
                session.add(new_company)
                session.commit()
                session.refresh(new_company)
                
                return jsonify({
                    "id": new_company.id,
                    "name": new_company.Name,
                    "adresse_id": new_company.Adresse,
                    "umsatz": new_company.Umsatz
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @unternehmen_bp.route('/<int:company_id>', methods=['PUT'])
    def update_company(company_id):
        """Update an existing company"""
        try:
            data = request.get_json()
            
            with db.session as session:
                company = session.execute(
                    select(tables.Unternehmen).where(tables.Unternehmen.id == company_id)
                ).scalar_one_or_none()
                
                if not company:
                    return jsonify({"error": "Company not found"}), 404
                
                # Update fields if provided
                if 'name' in data:
                    company.Name = data['name']
                if 'adresse_id' in data:
                    company.Adresse = data['adresse_id']
                if 'umsatz' in data:
                    company.Umsatz = data['umsatz']
                
                session.commit()
                session.refresh(company)
                
                return jsonify({
                    "id": company.id,
                    "name": company.Name,
                    "adresse_id": company.Adresse,
                    "umsatz": company.Umsatz
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @unternehmen_bp.route('/<int:company_id>', methods=['DELETE'])
    def delete_company(company_id):
        """Delete a company"""
        try:
            with db.session as session:
                company = session.execute(
                    select(tables.Unternehmen).where(tables.Unternehmen.id == company_id)
                ).scalar_one_or_none()
                
                if not company:
                    return jsonify({"error": "Company not found"}), 404
                
                session.delete(company)
                session.commit()
                
                return jsonify({"message": "Company deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return unternehmen_bp
