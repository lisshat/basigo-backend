# routes/booking_routes.py
from flask import Blueprint, request, jsonify
from redis.redis_client import validate_guest_session
from services.booking_service import store_booking

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/api/guest/book', methods=['POST'])
def book_ticket():
    data = request.json
    guest_uuid = data.get("guest_uuid")
    trip_id = data.get("trip_id")
    seat_number = data.get("seat_number")
    phone_number = data.get("phone_number")

    if validate_guest_session(guest_uuid):
        booking_info = store_booking(guest_uuid, trip_id, seat_number, phone_number)
        return jsonify({"status": "success", "booking_info": booking_info}), 201
    else:
        return jsonify({"status": "error", "message": "Session expired"}), 401
