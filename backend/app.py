from flask import Flask, jsonify
import backend.classes.aiven as aiven
from sqlalchemy import select
from backend.routes.products import init_routes as init_products
from backend.routes.adresse import init_routes as init_adresse
from backend.routes.person import init_routes as init_person
from backend.routes.unternehmen import init_routes as init_unternehmen
from backend.routes.kontakt import init_routes as init_kontakt
from backend.routes.terminart import init_routes as init_terminart
from backend.routes.termine import init_routes as init_termine
from backend.routes.protokoll import init_routes as init_protokoll
from backend.routes.teilnehmer import init_routes as init_teilnehmer
from backend.routes.medium import init_routes as init_medium
from backend.routes.anhang import init_routes as init_anhang
from backend.routes.wichtigkeit import init_routes as init_wichtigkeit
from backend.routes.auftrag import init_routes as init_auftrag
from backend.routes.auftragsposition import init_routes as init_auftragsposition

app = Flask(__name__)

# Initialize database connection
aiven_env = aiven.AivenEnvironment()
db = aiven.AivenDatabase(aiven_env)
db.connect()

# Register blueprints
app.register_blueprint(init_products(db))
app.register_blueprint(init_adresse(db))
app.register_blueprint(init_person(db))
app.register_blueprint(init_unternehmen(db))
app.register_blueprint(init_kontakt(db))
app.register_blueprint(init_terminart(db))
app.register_blueprint(init_termine(db))
app.register_blueprint(init_protokoll(db))
app.register_blueprint(init_teilnehmer(db))
app.register_blueprint(init_medium(db))
app.register_blueprint(init_anhang(db))
app.register_blueprint(init_wichtigkeit(db))
app.register_blueprint(init_auftrag(db))
app.register_blueprint(init_auftragsposition(db))


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to mobsys-backend-api",
        "version": "0.1.0",
        "endpoints": {
            "/": "Home",
            "/health": "Health check",
            "/api/products": "Products API",
            "/api/adresse": "Addresses API",
            "/api/person": "Persons API",
            "/api/unternehmen": "Companies API",
            "/api/kontakt": "Contacts API",
            "/api/terminart": "Appointment Types API",
            "/api/termine": "Appointments API",
            "/api/protokoll": "Protocols API",
            "/api/teilnehmer": "Participants API",
            "/api/medium": "Media API",
            "/api/anhang": "Attachments API",
            "/api/wichtigkeit": "Importance Levels API",
            "/api/auftrag": "Orders API",
            "/api/auftragsposition": "Order Items API"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with db.session as session:
            session.execute(select(1))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
