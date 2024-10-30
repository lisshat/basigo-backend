from flask import Flask
from firebase_admin import credentials, initialize_app
from .models import mongo_client

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.instance.config.Config')  # Load configuration from config.py

    # Initialize Firebase if needed
    firebase_credentials_path = app.config.get('FIREBASE_CREDENTIALS_JSON')
    if firebase_credentials_path:
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred)

    # Register Blueprints for APIs
    from apis.fetch_trips import fetch_trips_route
    from user_data.sign_in_user_data import sign_in_user_route
    from user_data.sign_up_user_data import sign_up_user_route
    from apis.dynamic_seat_booking.seat_layout import seat_layout_route

    app.register_blueprint(fetch_trips_route, url_prefix='/fetch_trips')
    app.register_blueprint(sign_in_user_route, url_prefix='/user/sign_in_user')
    app.register_blueprint(sign_up_user_route, url_prefix='/user/sign_up_user')
    app.register_blueprint(seat_layout_route, url_prefix='/seat_layout')

    # Make MongoDB client accessible via app context
    app.mongo_client = mongo_client

    return app
