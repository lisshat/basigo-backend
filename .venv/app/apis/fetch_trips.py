from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo")
db = client.basigoData # Select the BasiGo database
trips_collection = db.trips  # Select the trips collection

# API Route to fetch trips based on user input (e.g., route)
@app.route('/api/trips', methods=['GET'])
def fetch_trips():
    # Get input parameters
    departure_city = request.args.get('departure')
    destination_city = request.args.get('destination')

    # Check if the parameters are provided
    if not departure_city or not destination_city:
        return jsonify({"error": "Please provide both departure and destination cities"}), 400

    # Safe to call .strip() because we validated they exist
    departure_city = departure_city.strip()
    destination_city = destination_city.strip()

    # Construct the route string
    route = f"{departure_city} - {destination_city}"
    print(f"Querying trips for route: {route}")  # Debugging: print the route

    # Query the trips collection using a regex search
    try:
        trips = list(trips_collection.find({"route": {"$regex": route, "$options": "i"}}))
        print(f"Trips found: {len(trips)}")  # Debugging: print the number of trips found
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Convert ObjectId to string and extract departure/arrival from route
    trips_list = []
    for trip in trips:
        trip["_id"] = str(trip["_id"])  # Convert ObjectId to string

        # Extract departure and arrival from the route string
        if "route" in trip:
            cities = trip["route"].split(" - ")
            trip["departure"] = cities[0] if len(cities) > 0 else ""
            trip["arrival"] = cities[1] if len(cities) > 1 else ""

        # Convert amenities object to list of enabled amenities
        amenities_list = []
        if trip["amenities"].get("air_conditioning"):
            amenities_list.append("Air Conditioning")
        if trip["amenities"].get("disability_checking"):
            amenities_list.append("Disability Checking")
        if trip["amenities"].get("entertainment"):
            amenities_list.append("Entertainment")
        if trip["amenities"].get("snacks"):
            amenities_list.append("Snacks")
        if trip["amenities"].get("wifi"):
            amenities_list.append("WiFi")

        trip["amenities"] = amenities_list  # Replace amenities object with list

        trips_list.append(trip)

    return jsonify(trips_list)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
