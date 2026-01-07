from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

auftrag_bp = Blueprint('auftrag', __name__, url_prefix='/api/auftrag')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @auftrag_bp.route('', methods=['GET'])
    def get_orders():
        """Get all orders"""
        try:
            with db.session as session:
                orders = session.execute(select(tables.Auftrag)).scalars().all()
                result = []
                for order in orders:
                    result.append({
                        "id": order.id,
                        "bezeichnung": order.Bezeichnung,
                        "wichtigkeit_id": order.wichtigkeit,
                        "kontakt_id": order.Kontakt
                    })
                return jsonify({"orders": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftrag_bp.route('/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        """Get a single order by ID"""
        try:
            with db.session as session:
                order = session.execute(
                    select(tables.Auftrag).where(tables.Auftrag.id == order_id)
                ).scalar_one_or_none()
                
                if order:
                    return jsonify({
                        "id": order.id,
                        "bezeichnung": order.Bezeichnung,
                        "wichtigkeit_id": order.wichtigkeit,
                        "kontakt_id": order.Kontakt
                    }), 200
                else:
                    return jsonify({"error": "Order not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftrag_bp.route('', methods=['POST'])
    def create_order():
        """Create a new order"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['bezeichnung', 'wichtigkeit_id', 'kontakt_id']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_order = tables.Auftrag(
                    Bezeichnung=data['bezeichnung'],
                    wichtigkeit=data['wichtigkeit_id'],
                    Kontakt=data['kontakt_id']
                )
                session.add(new_order)
                session.commit()
                session.refresh(new_order)
                
                return jsonify({
                    "id": new_order.id,
                    "bezeichnung": new_order.Bezeichnung,
                    "wichtigkeit_id": new_order.wichtigkeit,
                    "kontakt_id": new_order.Kontakt
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftrag_bp.route('/<int:order_id>', methods=['PUT'])
    def update_order(order_id):
        """Update an existing order"""
        try:
            data = request.get_json()
            
            with db.session as session:
                order = session.execute(
                    select(tables.Auftrag).where(tables.Auftrag.id == order_id)
                ).scalar_one_or_none()
                
                if not order:
                    return jsonify({"error": "Order not found"}), 404
                
                # Update fields if provided
                if 'bezeichnung' in data:
                    order.Bezeichnung = data['bezeichnung']
                if 'wichtigkeit_id' in data:
                    order.wichtigkeit = data['wichtigkeit_id']
                if 'kontakt_id' in data:
                    order.Kontakt = data['kontakt_id']
                
                session.commit()
                session.refresh(order)
                
                return jsonify({
                    "id": order.id,
                    "bezeichnung": order.Bezeichnung,
                    "wichtigkeit_id": order.wichtigkeit,
                    "kontakt_id": order.Kontakt
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftrag_bp.route('/<int:order_id>', methods=['DELETE'])
    def delete_order(order_id):
        """Delete an order"""
        try:
            with db.session as session:
                order = session.execute(
                    select(tables.Auftrag).where(tables.Auftrag.id == order_id)
                ).scalar_one_or_none()
                
                if not order:
                    return jsonify({"error": "Order not found"}), 404
                
                session.delete(order)
                session.commit()
                
                return jsonify({"message": "Order deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return auftrag_bp
