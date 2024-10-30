from datetime import datetime

from firebase_admin import auth
from flask import Blueprint
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Initialize Firebase Admin SDK


# MongoDB setup
client = MongoClient(
    "mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo")
db = client.basigoData
users_collection = db.users

sign_in_user_route = Blueprint('sign_in_user', __name__)


@app.route('/signin', methods=['POST'])
def sign_in_user():
    token = request.json.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        # Get the user's email and other details
        firebase_user = auth.get_user(uid)
        email = firebase_user.email
        phone_number = firebase_user.phone_number

        # Check if user exists in MongoDB
        user = users_collection.find_one({"uid": uid})

        if not user:
            # New user: Create MongoDB record
            user_data = {
                "firebaseUid": uid,  # Firebase UID
                "email": email,  # User email
                "phoneNumber": phone_number,  # Phone number for MPESA transactions
                "createdAt": datetime.utcnow(),  # Timestamp for user creation
                "lastSignIn": datetime.utcnow(),  # Timestamp for last sign-in
                "tickets": [],  # List of tickets
                "bookings": [],  # List of bookings (optional)
                "status": "active"  # User status
            }

            users_collection.insert_one(user_data)
        else:
            # Existing user: Update lastSignIn timestamp
            users_collection.update_one(
                {"uid": uid},
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


if __name__ == "__main__":
    app.run(debug=True, port=5005)
