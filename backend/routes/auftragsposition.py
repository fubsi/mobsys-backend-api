from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

auftragsposition_bp = Blueprint('auftragsposition', __name__, url_prefix='/api/auftragsposition')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @auftragsposition_bp.route('', methods=['GET'])
    def get_order_items():
        """Get all order items with resolved order and product data"""
        try:
            with db.session as session:
                items = session.execute(select(tables.Auftragsposition)).scalars().all()
                result = []
                for item in items:
                    item_data = {
                        "id": item.id,
                        "auftrag_id": item.Auftrag,
                        "produkt_id": item.Produkt
                    }
                    
                    # Resolve Auftrag foreign key
                    auftrag = session.execute(
                        select(tables.Auftrag).where(tables.Auftrag.id == item.Auftrag)
                    ).scalar_one_or_none()
                    
                    if auftrag:
                        item_data["auftrag"] = {
                            "id": auftrag.id,
                            "bezeichnung": auftrag.Bezeichnung,
                            "wichtigkeit_id": auftrag.wichtigkeit,
                            "kontakt_id": auftrag.Kontakt,
                            "termin_id": auftrag.terminid
                        }
                    
                    # Resolve Produkt foreign key
                    produkt = session.execute(
                        select(tables.Produkt).where(tables.Produkt.id == item.Produkt)
                    ).scalar_one_or_none()
                    
                    if produkt:
                        item_data["produkt"] = {
                            "id": produkt.id,
                            "name": produkt.Bezeichnung,
                            "price": float(produkt.Preis) if produkt.Preis else None
                        }
                    
                    result.append(item_data)
                return jsonify({"order_items": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftragsposition_bp.route('/<int:item_id>', methods=['GET'])
    def get_order_item(item_id):
        """Get a single order item by ID with resolved order and product data"""
        try:
            with db.session as session:
                item = session.execute(
                    select(tables.Auftragsposition).where(tables.Auftragsposition.id == item_id)
                ).scalar_one_or_none()
                
                if item:
                    item_data = {
                        "id": item.id,
                        "auftrag_id": item.Auftrag,
                        "produkt_id": item.Produkt
                    }
                    
                    # Resolve Auftrag foreign key
                    auftrag = session.execute(
                        select(tables.Auftrag).where(tables.Auftrag.id == item.Auftrag)
                    ).scalar_one_or_none()
                    
                    if auftrag:
                        item_data["auftrag"] = {
                            "id": auftrag.id,
                            "bezeichnung": auftrag.Bezeichnung,
                            "wichtigkeit_id": auftrag.wichtigkeit,
                            "kontakt_id": auftrag.Kontakt,
                            "termin_id": auftrag.terminid
                        }
                    
                    # Resolve Produkt foreign key
                    produkt = session.execute(
                        select(tables.Produkt).where(tables.Produkt.id == item.Produkt)
                    ).scalar_one_or_none()
                    
                    if produkt:
                        item_data["produkt"] = {
                            "id": produkt.id,
                            "name": produkt.Bezeichnung,
                            "price": float(produkt.Preis) if produkt.Preis else None
                        }
                    
                    return jsonify(item_data), 200
                else:
                    return jsonify({"error": "Order item not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftragsposition_bp.route('', methods=['POST'])
    def create_order_item():
        """Create a new order item"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['auftrag_id', 'produkt_id']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_item = tables.Auftragsposition(
                    Auftrag=data['auftrag_id'],
                    Produkt=data['produkt_id']
                )
                session.add(new_item)
                session.commit()
                session.refresh(new_item)
                
                return jsonify({
                    "id": new_item.id,
                    "auftrag_id": new_item.Auftrag,
                    "produkt_id": new_item.Produkt
                }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftragsposition_bp.route('/<int:item_id>', methods=['PUT'])
    def update_order_item(item_id):
        """Update an existing order item"""
        try:
            data = request.get_json()
            
            with db.session as session:
                item = session.execute(
                    select(tables.Auftragsposition).where(tables.Auftragsposition.id == item_id)
                ).scalar_one_or_none()
                
                if not item:
                    return jsonify({"error": "Order item not found"}), 404
                
                # Update fields if provided
                if 'auftrag_id' in data:
                    item.Auftrag = data['auftrag_id']
                if 'produkt_id' in data:
                    item.Produkt = data['produkt_id']
                
                session.commit()
                session.refresh(item)
                
                return jsonify({
                    "id": item.id,
                    "auftrag_id": item.Auftrag,
                    "produkt_id": item.Produkt
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auftragsposition_bp.route('/<int:item_id>', methods=['DELETE'])
    def delete_order_item(item_id):
        """Delete an order item"""
        try:
            with db.session as session:
                item = session.execute(
                    select(tables.Auftragsposition).where(tables.Auftragsposition.id == item_id)
                ).scalar_one_or_none()
                
                if not item:
                    return jsonify({"error": "Order item not found"}), 404
                
                session.delete(item)
                session.commit()
                
                return jsonify({"message": "Order item deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return auftragsposition_bp
