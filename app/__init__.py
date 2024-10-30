from flask import Flask
from firebase_admin import credentials, initialize_app
from .models.models import mongo_client
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.instance.config.Config')  # Load configuration from config.py

    # Load Firebase credentials from environment variable
    firebase_creds_b64 = os.getenv('FIREBASE_CREDENTIALS')
    if firebase_creds_b64:
        # Decode the base64 string
        firebase_creds_json = base64.b64decode(firebase_creds_b64).decode('utf-8')
        # Parse the JSON
        cred_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(cred_dict)
        initialize_app(cred)
    else:
        raise ValueError("Firebase credentials not found in environment variables")

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
