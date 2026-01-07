from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

anhang_bp = Blueprint('anhang', __name__, url_prefix='/api/anhang')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @anhang_bp.route('', methods=['GET'])
    def get_attachments():
        """Get all attachments"""
        try:
            with db.session as session:
                attachments = session.execute(select(tables.Anhang)).scalars().all()
                result = []
                for attachment in attachments:
                    result.append({
                        "id": attachment.id,
                        "protokoll_id": attachment.Protokoll,
                        "medium_id": attachment.Medium
                    })
                return jsonify({"attachments": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @anhang_bp.route('/<int:attachment_id>', methods=['GET'])
    def get_attachment(attachment_id):
        """Get a single attachment by ID"""
        try:
            with db.session as session:
                attachment = session.execute(
                    select(tables.Anhang).where(tables.Anhang.id == attachment_id)
                ).scalar_one_or_none()
                
                if attachment:
                    return jsonify({
                        "id": attachment.id,
                        "protokoll_id": attachment.Protokoll,
                        "medium_id": attachment.Medium
                    }), 200
                else:
                    return jsonify({"error": "Attachment not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @anhang_bp.route('', methods=['POST'])
    def create_attachment():
        """Create a new attachment"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['protokoll_id', 'medium_id']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_attachment = tables.Anhang(
                    Protokoll=data['protokoll_id'],
                    Medium=data['medium_id']
                )
                session.add(new_attachment)
                session.commit()
                session.refresh(new_attachment)
                
                return jsonify({
                    "id": new_attachment.id,
                    "protokoll_id": new_attachment.Protokoll,
                    "medium_id": new_attachment.Medium
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @anhang_bp.route('/<int:attachment_id>', methods=['PUT'])
    def update_attachment(attachment_id):
        """Update an existing attachment"""
        try:
            data = request.get_json()
            
            with db.session as session:
                attachment = session.execute(
                    select(tables.Anhang).where(tables.Anhang.id == attachment_id)
                ).scalar_one_or_none()
                
                if not attachment:
                    return jsonify({"error": "Attachment not found"}), 404
                
                # Update fields if provided
                if 'protokoll_id' in data:
                    attachment.Protokoll = data['protokoll_id']
                if 'medium_id' in data:
                    attachment.Medium = data['medium_id']
                
                session.commit()
                session.refresh(attachment)
                
                return jsonify({
                    "id": attachment.id,
                    "protokoll_id": attachment.Protokoll,
                    "medium_id": attachment.Medium
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @anhang_bp.route('/<int:attachment_id>', methods=['DELETE'])
    def delete_attachment(attachment_id):
        """Delete an attachment"""
        try:
            with db.session as session:
                attachment = session.execute(
                    select(tables.Anhang).where(tables.Anhang.id == attachment_id)
                ).scalar_one_or_none()
                
                if not attachment:
                    return jsonify({"error": "Attachment not found"}), 404
                
                session.delete(attachment)
                session.commit()
                
                return jsonify({"message": "Attachment deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return anhang_bp
