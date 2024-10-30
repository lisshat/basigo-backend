from datetime import datetime
from firebase_admin import auth, exceptions
from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Define the blueprint for signing up users
sign_up_user_route = Blueprint('sign_up_user', __name__)

@sign_up_user_route.route('/signup', methods=['POST'])
def sign_up_user():
    try:
        # Parse request data
        email = request.json.get("email")
        phone_number = request.json.get("phoneNumber")
        password = request.json.get("password")

        # Ensure phone number is in E.164 format
        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"

        # Create Firebase user
        firebase_user = auth.create_user(
            email=email,
            phone_number=phone_number,
            password=password
        )

        uid = firebase_user.uid

        # Access MongoDB through Flask's app context
        mongo_client = request.app.mongo_client
        db = mongo_client.basigoData
        users_collection = db.users

        # Store user details in MongoDB
        user_data = {
            "firebaseUid": uid,
            "email": email,
            "phoneNumber": phone_number,
            "createdAt": datetime.utcnow(),
            "tickets": [],
            "bookings": [],
            "status": "active"
        }
        users_collection.insert_one(user_data)

        return jsonify({"message": "User signed up successfully", "uid": uid}), 200

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400

    except exceptions.FirebaseError as fe:
        print(f"FirebaseError: {fe}")
        return jsonify({"error": "Firebase error occurred"}), 500

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
