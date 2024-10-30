# routes/ticket_routes.py
from flask import Blueprint, jsonify
from redis.redis_client import validate_guest_session
from services.ticket_service import generate_ticket

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/api/guest/ticket/<guest_uuid>', methods=['GET'])
def get_ticket(guest_uuid):
    if validate_guest_session(guest_uuid):
        ticket = generate_ticket(guest_uuid)
        if ticket:
            return jsonify(ticket)
        else:
            return jsonify({"status": "error", "message": "No ticket found"}), 404
    else:
        return jsonify({"status": "error", "message": "Session expired"}), 401
