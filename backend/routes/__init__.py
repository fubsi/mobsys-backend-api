"""
Routes module for mobsys-backend-api
Contains all API route blueprints
"""

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

__all__ = [
    'init_products',
    'init_adresse',
    'init_person',
    'init_unternehmen',
    'init_kontakt',
    'init_terminart',
    'init_termine',
    'init_protokoll',
    'init_teilnehmer',
    'init_medium',
    'init_anhang',
    'init_wichtigkeit',
    'init_auftrag',
    'init_auftragsposition'
]
