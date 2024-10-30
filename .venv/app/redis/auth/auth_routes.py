from flask import Blueprint, request, jsonify
import uuid
from redis.redis_client import cache_user_session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/guest-login', methods=['POST'])
def guest_login():
    session_id = str(uuid.uuid4())
    user_data = {
        "session_id": session_id,
        "is_guest": True
    }
    cache_user_session(session_id, user_data)
    return jsonify({"session_id": session_id, "message": "Logged in as guest"}), 200
