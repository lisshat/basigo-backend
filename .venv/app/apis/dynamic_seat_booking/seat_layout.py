from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo")
db = client.basigoData
bus_collection = db.bus

# API to get basic seat layout info (totalSeats only) for quick UI rendering
@app.route('/api/bus/<busId>', methods=['GET'])
def get_basic_seat_layout(busId):
    bus = bus_collection.find_one({"_id": busId})  # Fetch bus seat layout by busId
    if bus and 'seats' in bus and 'total' in bus['seats']:
        return jsonify({"totalSeats": bus['seats']['total']})  # Return the total seats from the seats map
    else:
        return jsonify({"error": "Bus or seat information not found"}), 404


@app.route('/api/bus/detailed-layout/<busId>', methods=['GET'])
def get_detailed_seat_layout(busId):
    bus = bus_collection.find_one({"_id": busId})
    print("Received BusId:",busId)
    if bus and 'seats' in bus:
        seats_data = bus['seats']
        print("Returning seat layout:", seats_data)
        seats_data.pop('total', None)  # Remove 'total' if it exists
        return jsonify(seats_data)
    else:
        return jsonify({"error": "Bus not found"}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5002)
