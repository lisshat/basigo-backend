from datetime import datetime
from firebase_admin import auth
from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Define the blueprint for signing in users
sign_in_user_route = Blueprint('sign_in_user', __name__)

@sign_in_user_route.route('/signin', methods=['POST'])
def sign_in_user():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        # Get the user's email and other details from Firebase
        firebase_user = auth.get_user(uid)
        email = firebase_user.email
        phone_number = firebase_user.phone_number

        # Access MongoDB through Flask's app context
        mongo_client = request.app.mongo_client
        db = mongo_client.basigoData
        users_collection = db.users

        # Check if user exists in MongoDB
        user = users_collection.find_one({"firebaseUid": uid})

        if not user:
            # New user: Create MongoDB record
            user_data = {
                "firebaseUid": uid,
                "email": email,
                "phoneNumber": phone_number,
                "createdAt": datetime.utcnow(),
                "lastSignIn": datetime.utcnow(),
                "tickets": [],
                "bookings": [],
                "status": "active"
            }
            users_collection.insert_one(user_data)
        else:
            # Existing user: Update lastSignIn timestamp
            users_collection.update_one(
                {"firebaseUid": uid},
                {"$set": {"lastSignIn": datetime.utcnow()}}
            )

        # Return success response
        return jsonify({"message": "User signed in successfully", "uid": uid, "email": email}), 200

    except auth.AuthError as e:
        print("Firebase Authentication error:", e)
        return jsonify({"error": "Authentication failed"}), 401
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
