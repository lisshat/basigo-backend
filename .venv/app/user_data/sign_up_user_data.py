from flask import Flask, request, jsonify
from firebase_admin import auth, credentials, initialize_app, exceptions
from pymongo import MongoClient
from datetime import datetime
from instance.config import Config

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_JSON)
initialize_app(cred)

# MongoDB setup
client = MongoClient("mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo")
db = client.basigoData
users_collection = db.users

@app.route('/signup', methods=['POST'])
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

if __name__ == "__main__":
    app.run(debug=True, port=5006)
