# app/__init__.py
from flask import Flask
from .models import mongo_client  # Import the MongoDB client instance

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    # Register Blueprints for Redis-based authentication, booking, and tickets
    from redis.auth.auth_routes import auth_bp
    from redis.routes.booking_routes import booking_bp
    from redis.routes.ticket_routes import ticket_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(ticket_bp, url_prefix='/ticket')

    # Make MongoDB client accessible via app context
    app.mongo_client = mongo_client

    return app
