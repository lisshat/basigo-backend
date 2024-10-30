from flask import Blueprint, jsonify, current_app

# Define the blueprint for seat layout routes
seat_layout_route = Blueprint('seat_layout', __name__)

# API to get basic seat layout info (totalSeats only) for quick UI rendering
@seat_layout_route.route('/bus/<busId>', methods=['GET'])
def get_basic_seat_layout(busId):
    # Access MongoDB through the Flask app context
    mongo_client = current_app.mongo_client
    db = mongo_client.basigoData
    bus_collection = db.bus

    # Fetch bus seat layout by busId
    bus = bus_collection.find_one({"_id": busId})
    if bus and 'seats' in bus and 'total' in bus['seats']:
        return jsonify({"totalSeats": bus['seats']['total']})
    else:
        return jsonify({"error": "Bus or seat information not found"}), 404

# API to get detailed seat layout info
@seat_layout_route.route('/bus/detailed-layout/<busId>', methods=['GET'])
def get_detailed_seat_layout(busId):
    # Access MongoDB through the Flask app context
    mongo_client = current_app.mongo_client
    db = mongo_client.basigoData
    bus_collection = db.bus

    print("Received BusId:", busId)
    bus = bus_collection.find_one({"_id": busId})
    if bus and 'seats' in bus:
        seats_data = bus['seats']
        print("Returning seat layout:", seats_data)
        seats_data.pop('total', None)  # Remove 'total' if it exists
        return jsonify(seats_data)
    else:
        return jsonify({"error": "Bus not found"}), 404
