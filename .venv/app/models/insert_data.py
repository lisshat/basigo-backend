from datetime import datetime, timedelta
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient('mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo')
db = client['basigoData']  # replace with your actual MongoDB database name
collection = db['trips']  # replace with your collection name

# Function to update realistic dates and times for round trips
def update_trip_dates():
    trips = collection.find({"oneWay": False})  # Find round trips where oneWay is False

    for trip in trips:
        # Parse existing departure and return dates
        departure_date = datetime.strptime(trip['departure'], "%Y-%m-%d")
        return_date = datetime.strptime(trip['returnDate'], "%Y-%m-%d")

        # Ensure the return date is after the departure date
        if return_date <= departure_date:
            # Set a new return date with an offset of 1-7 days after the departure
            new_return_date = departure_date + timedelta(days=1 + (return_date - departure_date).days)

            # Add realistic time (between 6 AM and 11 PM) for departure and return times
            departure_time = departure_date + timedelta(hours=6)  # start at 6 AM
            return_time = new_return_date + timedelta(hours=12)  # assume trip duration of 12 hours

            # Update the document in MongoDB
            collection.update_one(
                {"_id": trip["_id"]},
                {"$set": {
                    "departure": departure_date.strftime("%Y-%m-%d"),
                    "returnDate": new_return_date.strftime("%Y-%m-%d"),
                    "departureTime": departure_time.strftime("%H:%M"),
                    "returnTime": return_time.strftime("%H:%M")  # Assuming you want to track return time
                }}
            )

    return "Trip dates updated successfully!"

# Run the function to update the trip dates
print(update_trip_dates())
